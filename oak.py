#!/usr/bin/env python3

import discord


class OakClient(discord.Client):
    async def on_ready(self):
        await self.change_status(game=discord.Game(name='Pokedex'))
        print('Logged in as {}:{}'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        if not self.user in message.mentions:
            return
        if not message.content.startswith('<@421668164959731712>'):
            return
        if message.author.top_role.name not in ['admin', 'Modo']:
            channel = message.channel
            await self.send_message(channel, "You can't use that here !")
            return
        try:
            command = message.content.strip('\n').split()[1]
            if command == 'hello':
                await self.say_hello(message)
            elif command == 'clean':
                await self.clean_role(message)
            return

        except:
            print('Unexpected error')
            raise

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
            if int(c.id) == 283349483670994945:
                channel = c
            elif int(c.id) == 343308060661645313:
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

    async def clean_role(self, message):
        await self.change_presence(status='idle')
        try:
            role_str = message.content.strip('\n').split()[2]
            for r in message.server.roles:
                if r.mention == role_str:
                    role = r
                    break
            for member in message.server.members:
                try:
                    await self.remove_roles(member, role)
                except discord.HTTPException:
                    print('Unable to remove role for {}'.format(member))
                    pass
            await self.send_message(message.channel, 'Cleaned {}'.format(role))
            await self.change_presence(status='online')
        except IndexError:
            await self.change_presence(status=online)
            raise
        return

    async def assign_channel(self, message):
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


if __name__ == '__main__':
    main()


