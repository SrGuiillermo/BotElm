from twitchio.ext import commands
from random import randint
from asyncio import sleep
from requests import get


TOKEN = open("TMI.txt", "r").read()
CHANNELS = open("CHANNELS.txt", "r").read().split(",")
AUTHORIZED = open("AUTHORIZED.txt", "r").read().split(",")
CONSOLE_MSG_STATUS = [1]
COPY_COM_STATUS = [1]
COPY_COM_TARGET = []
CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])


class Bot(commands.Bot):


    def __init__(self):
        super().__init__(
            token = TOKEN,
            prefix = "$",
            initial_channels = CHANNELS
            )
        print("BOT READY")

    async def event_message(self, message):

        #Variables
        split_msg = message.content.lower().split(" ")
        elm = self.get_channel("ElmiilloR")
        console_msg_status = CONSOLE_MSG_STATUS
        copy_com_status = COPY_COM_STATUS
        copy_com_target = COPY_COM_TARGET
        chatters = CHATTERS

        #Console msg
        if message.echo:
            return
        if console_msg_status[0] == 0:
            print(f"<{message.channel.name}> {message.author.name} : {message.content}")
        await self.handle_commands(message)
        
        #Console msg switch
        if message.author.name == "srguillermo" and "$con" in split_msg:
            if console_msg_status[0] == 1:
                console_msg_status[0] = 0
            elif console_msg_status[0] == 0:
                console_msg_status[0] = 1


        #Copy Command
        if message.author.name == "srguillermo" and ("$copystop" or "$cs" in split_msg):
            copy_com_status[0] = 1
        if message.author.name == "srguillermo" and "$copy" in split_msg:
            copy_com_status[0] = 0
            copy_com_target[0] = split_msg[-1]
        if copy_com_status[0] == 0 and message.author.name == copy_com_target[-1]:
            await message.channel.send(f"FeelsSpecialMan : {message.content}")

        #Act viewers list
        if message.author.name == "srguillermo" and "$act" in split_msg:
            chatters = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
            chatters.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
    
    
    #Namess
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

    
    #Nunban
    @commands.command()
    async def nunban(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[1]
            try:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/unban {username}")
            except IndexError:
                await ctx.send(f"/unban {username}")
        else: pass


    #Linktree spam command
    @commands.command(aliases=["lt"])
    async def linktree(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name == "srguillermo":
            for i in range(int(split_msg[-1])):
                await self.get_channel("ElmiilloR").send("https://linktr.ee/elmillor Bedge Zzz ")
                await sleep(0.1)

    #Random
    @commands.command(aliases=["gr", "printrandom"])
    async def getrandom(self, ctx: commands.Context):
        chatters = CHATTERS
        await ctx.send(chatters[randint(0, len(chatters))])
    
    
    #SoloQChallenge
    @commands.command(aliases=["sqc"])
    async def soloq(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name == "srguillermo":
            for i in range(int(split_msg[-1])):
                await self.get_channel("ElmiilloR").send("La web PeepoGlad 👉 https://soloqchallenge.gg ")
                await sleep(0.1)
    
    
    #Exceptions            
    @commands.command(aliases=["copystop", "cs", "copy", "act"])
    async def con(self, ctx: commands.Context):
        print()        


if __name__ == "__main__":
    bot = Bot()  
    bot.run()