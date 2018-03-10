#!/usr/bin/env python3

import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {}:{}'.format(self.user.name, self.user.id))
        self.roles = {role.name: role for role in list(self.servers)[0].roles}
        self.channels = {channel.name: channel for channel in
                         list(self.servers)[0].channels}

    async def on_message(self, message):
        if not self.user in message.mentions:
            return
        if not message.content.startswith('<@421668164959731712>'):
            return
        content = message.content.strip('<@421668164959731712>').strip()
        if content in self.roles.keys() and content in self.channels.keys():
            await self.add_roles(message.author, self.roles[content])
            await self.send_message(self.channels[content], 'Welcome here
                                    {}'.format( message.author.mention))


def main():
    client = MyClient()
    try:
        with open('token') as token:
            tok = token.readline()
            client.run(tok.strip())
    except (KeyboardInterrupt, SystemExit):
        client.close()


if __name__ == '__main__':
    main()


