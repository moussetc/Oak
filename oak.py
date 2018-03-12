#!/usr/bin/env python3

import discord


class OakClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {}:{}'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        if not self.user in message.mentions:
            return
        if not message.content.startswith('<@421668164959731712>'):
            return
        try:
            await self.assign_channel(message)
            return
        except:
            print('Unexpected error')
            raise

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


