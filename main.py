from twitchio.ext import commands
import random
from asyncio import sleep


TOKEN = open("TMI.txt", "r").read()
CHANNELS = open("CHANNELS.txt", "r").read().split(",")
AUTHORIZED = open("AUTHORIZED.txt", "r").read().split(",")
CONSOLE_MSG_STATUS = [1]

class Bot(commands.Bot):


    def __init__(self):
        super().__init__(
            token = TOKEN,
            prefix = "$",
            initial_channels = CHANNELS
            )

    async def event_message(self, message):
        #Variables
        split_msg = message.content.lower().split(" ")
        elm = self.get_channel("ElmiilloR")
        console_msg_status = CONSOLE_MSG_STATUS

        #Console msg
        if message.echo:
            return
        if console_msg_status[0] == 0:
            print("<{}> {} : {}".format(message.channel.name, message.author.name, message.content))
        await self.handle_commands(message)

        if message.author.name == "srguillermo" and message.channel.name == "srguillermo" and "$con" in split_msg:
            if console_msg_status[0] == 1:
                console_msg_status[0] = 0
            elif console_msg_status[0] == 0:
                console_msg_status[0] = 1

    @commands.command()
    async def namess(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[1]
            duration = split_msg[2]
            if int(duration) > 300:
                duration = 300
            try:
                channel = self.get_channel(split_msg[3])
                await channel.send(f"/timeout {username} {duration}")
            except IndexError:
                await ctx.send(f"/timeout {username} {duration}")
        else: pass


    @commands.command(aliases=["lt"])
    async def linktree(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name == "srguillermo":
            for i in range(int(split_msg[-1])):
                await ctx.send("https://linktr.ee/elmillor Bedge Zzz ")
                await sleep(0.1)

                
    @commands.command(aliases=[])
    async def con(self, ctx: commands.Context):
        print()        


if __name__ == "__main__":
    bot = Bot()  
    bot.run()