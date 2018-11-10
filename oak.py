#!/usr/bin/env python3

import discord
from typing import List

import db
from text_recognition import detect_text, find_raid_fields, find_pokestop, find_pokemon
from config import roles_admin, roles_sectors, raid_ex_channels, raid_channel, quest_channel, assignment_channel, rules_channel
from utils import logger

def build_roles(roles):
    role_match = {}
    for r in roles:
        if int(r.id) in roles_sectors:
            role_match[r.name.lower()] = r
    return role_match


class OakClient(discord.Client):
    async def on_ready(self):
        for s in self.servers:
            self.sectors = build_roles(s.roles)
        await self.change_presence(game=discord.Game(name='Pokedex'))
        logger.info('Logged in as %s:%s', self.user.name, self.user.id)

    async def check_author(self, message):
        if message.author.top_role.name not in roles_admin:
            channel = message.channel
            await self.send_message(channel, "You can't use that here !")
            return False
        else:
            return True

    async def on_message_edit(self, before, after):
        await self.on_message(after)

    async def on_message(self, message):
        if int(message.channel.id) == raid_channel:
            await self.add_raid(message)
            return
        elif int(message.channel.id) == quest_channel:
            await self.add_quest(message)
            return
        elif not self.user in message.mentions:
            return
        try:
            command = message.content.strip('\n').split()[1]
            if command == 'hello':
                await self.say_hello(message)
            elif command == 'clean':
                is_allowed = await self.check_author(message)
                if is_allowed:
                    await self.clean_role(message)
            elif command == 'join':
                await self.add_sector(message)
            return
        except Exception as ex:
            logger.error('on_message failed: %s', str(ex))
            raise

    async def add_raid(self, message):
        logger.debug("add_raid request")
        if message.attachments == []:
            return
        image_url = message.attachments[0]['proxy_url']
        raid_description = detect_text(image_url)
        res = find_raid_fields(raid_description)
        logger.debug("add_raid: detected raid description=%s | res=%s", raid_description, res)
        missing_infos = []
        if res['boss'] is None:
            missing_infos.append('raid boss')
        if res['gym'] is None:
            missing_infos.append('gym name')
        if res['time'] is None:
            missing_infos.append('end time')
        if missing_infos != []:
            await self.send_message(message.channel,
                    "Sorry I wasn't able to read {}.".format(', '.join(missing_infos)))
        else:
            try:
                db.add_raid(res['boss'], res['gym'], res['time'])
                await self.send_message(message.channel,
                "Adding {} raid on {} ending in {}".format(
                    res['boss'], res['gym'], res['time']))
            except Exception as ex:
                await self.send_message(message.channel,
                "Something went wrong adding {} on {} ending in {}".format(
                    res['boss'], res['gym'], res['time']))
                logger.error("add_raid failed to add raid to db:%s", str(ex))

    async def add_quest(self, message):
        logger.debug("add_quest request")
        if message.attachments == []:
            logger.debug("Can't add quest without image attachment")
            return
        try:
            pokemon = find_pokemon(message.content)
            if pokemon is None:
                logger.debug('No matching pokemon found, do nothing')
                return
            image_url = message.attachments[0]['proxy_url']
            quest_pokestop = detect_text(image_url)
            pokestop = find_pokestop(quest_pokestop)
            logger.debug("Add quest for %s at %s", pokemon, pokestop)
            if not pokestop:
                await self.send_message(message.channel, "Sorry I didn't find any matching pokestop")
                logger.debug("No pokestop found, so we're not doing anything.")
                return
            db.add_quest(pokestop, pokemon)
            await self.add_reaction(message, u'\u2705')
        except Exception:
            logger.exception("add_quest failed")

    async def on_member_join(self, member):
        await self.welcome(member)
        return

    async def say_hello(self, message):
        channel = message.channel
        await self.send_message(channel, 'Hello trainer !')
        return

    async def welcome(self, member):
        channel = None
        rules = None
        for c in self.get_all_channels():
            if int(c.id) == assignment_channel:
                channel = c
            elif int(c.id) == rules_channel:
                rules = c

        welcome = (
            'Hello {0} !\n'
            'Bienvenue sur le discord de Pokémon Go Grenoble, '
            'poste un screenshot de ton perso IG dans {1}'
            ' et pense à bien **lire le {2} et les messages épinglés** !'
            '\n----------\n'
            'Welcome to Pokémon Go Grenoble\'s discord server, '
            'please send a screenshot of your IG avatar in {1}'
            ' and **read both {2} and the pinned messages** !'
        )

        await self.send_message(channel,
            welcome.format(member.mention, channel.mention, rules.mention))
        return

    async def recreate_role(self, message, role):
        role_name = role.name
        if role.name in raid_ex_channels:
            server = message.server
            channel = discord.utils.get(server.channels, name=role_name)
            overwrite = channel.overwrites_for(role)
            await self.delete_role(server, role)
            role = await self.create_role(server, name=role_name, mentionable=True)
            await self.edit_channel_permissions(channel, role, overwrite)
            await self.add_reaction(message, u'\U0001F44C')
        else:
            return
            

    async def clean_role(self, message):
        role_str = message.content.strip('\n').split()[2]
        role = None
        for r in message.server.roles:
            if r.mention == role_str:
                role = r
                break
        if role is None:
            await self.send_message(message.channel,
                'Sorry I can\'t find {}'.format(role_str))
            return
        await self.recreate_role(message, role)

    async def add_sector(self, message):
        try:
            channel_str = message.content.strip('\n').split()[2]
            channel_name = channel_str.replace('#', '')
            if channel_name not in self.sectors.keys():
                await self.send_message(message.channel,
                    'Sorry there is no {} sector'.format(channel_str))
            else:
                role = self.sectors[channel_name.lower()]
                await self.add_roles(message.author, role)
                await self.add_reaction(message, u"\U0001F44B")
                channel = discord.utils.get(message.server.channels, name=channel_name)
                await self.send_message(channel,
                    'Welcome here {}'.format(message.author.mention) + u'\U0001F44B')
        except IndexError:
            raise
        return

    async def assign_sector(self, message):
        content = message.content.strip('<@421668164959731712>').strip()
        for r in message.server.roles:
            if content == r.name:
                role = r
                break
        if role:
            await self.add_roles(message.author, role)
            for c in message.server.channels:
                if content == c.name:
                    channel = c
            if channel:
                stats = self.get_stats(message.server, role)
                mess = 'Welcome here {} we currently have {} valors, {} mystics and {} instincts'.format(
                        message.author.mention, stats[0], stats[1], stats[2])
                await self.send_message(channel, mess)

    def get_stats(self, server, role):
        for r in server.roles:
            if r.name == 'Valor':
                valor = r
            elif r.name == 'Mystic':
                mystic = r
            elif r.name == 'Instinct':
                instinct = r
        red = 0
        blue = 0
        yellow = 0
        for member in server.members:
            roles = member.roles
            if role in roles:
                if valor in roles:
                    red += 1
                elif mystic in roles:
                    blue += 1
                elif instinct in roles:
                    yellow += 1
        return (red, blue, yellow)


def main():
    oak = OakClient()
    try:
        with open('token') as token:
            tok = token.readline()
            oak.run(tok.strip())
    except (KeyboardInterrupt, SystemExit):
        oak.close()
    except Exception as ex:
        logger.error("Could not start Oak bot:%s", str(ex))

if __name__ == '__main__':
    main()


