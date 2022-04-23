from twitchio.ext import commands
import random
from asyncio import sleep


TOKEN = open("TMI.txt", "r").read()
CHANNELS = open("CHANNELS.txt", "r").read().split(",")
AUTHORIZED = open("AUTHORIZED.txt", "r").read().split(",")


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
        
        #Console msg
        if message.echo:
            return
        print("<{}> {} : {}".format(message.channel.name, message.author.name, message.content))
        await self.handle_commands(message)


    @commands.command()
    async def namess(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        elm = self.get_channel("ElmiilloR")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[-2]
            duration = split_msg[-1]
            if int(duration) > 300:
                duration = 300
            await elm.send(f"/timeout {username} {duration}")
        else: pass


    @commands.command(aliases=["lt"])
    async def linktree(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name == "srguillermo":
            for i in range(int(split_msg[-1])):
                await ctx.send("https://linktr.ee/elmillor Bedge Zzz ")
                await sleep(0.1)        


if __name__ == "__main__":
    bot = Bot()  
    bot.run()