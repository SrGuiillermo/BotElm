from twitchio.ext import commands
from random import randint
from asyncio import sleep
from requests import get
from config import config

TOKEN = config["tmi"]
CHANNELS = config["channels"]
AUTHORIZED = config["authorized"]
CONSOLE_MSG_STATUS = [1]
COPY_COM_STATUS = [1]
COPY_COM_TARGET = [0]
CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
WORD_LIST_STATUS = [1]
try:
    WORD_LIST = open("word_list.txt", "r").read().split(",")
except FileNotFoundError:
    temp = ["3600"]
    with open("word_list.txt", "w") as f:
        f.writelines(temp)
    WORD_LIST = temp

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
        console_msg_status = CONSOLE_MSG_STATUS
        copy_com_status = COPY_COM_STATUS
        copy_com_target = COPY_COM_TARGET
        chatters = CHATTERS
        word_list = WORD_LIST
        word_list_status = WORD_LIST_STATUS

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
        
        #Word list switch
        if message.author.name == "srguillermo" and "$ws" in split_msg:
            if word_list_status[0] == 1:
                word_list_status[0] = 0
                print("Word command online")
            elif word_list_status[0] == 0:
                word_list_status[0] = 1
                print("Word command offline")
        
        #Word
        if message.author.name == "srguillermo" and "$word" in split_msg:

            if split_msg[1] == "time":
                word_list[0] = split_msg[-1]
                with open("word_list.txt", "w") as f:
                    f.write(",".join(word_list))
                print(f"Time in word command changed to {split_msg[-1]}")

            if split_msg[1] == "add":
                for i in range(2, len(split_msg)):
                    if split_msg[i] not in word_list:
                        word_list.append(split_msg[i])
                        print(f"{split_msg[i]} added to word list")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(word_list))
            
            if split_msg[1] == "remove":
                for i in range(2, len(split_msg)):
                    if split_msg[i] in word_list:
                        for a in range(len(word_list)):
                            if split_msg[i] == word_list[a]:
                                del word_list [a]
                                print(f"{word_list[a]} removed from word list")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(word_list))
            
            if split_msg[1] == "clean":
                for i in range(1, len(word_list)):
                    del word_list[i]
                    print(f"Word list cleaned")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(word_list))
        
        if word_list_status[0] == 0:
            incl = False
            for i in range(1, len(word_list)):
                if word_list[i] in split_msg:
                    incl = True
            if incl == True:
                await message.channel.send(f"/timeout {message.author.name} {word_list[0]}")
            incl = False


        #Copy Command
        if message.author.name == "srguillermo" and "$cs" in split_msg:
            copy_com_status[0] = 1
            print("Copy command stopped")
        if message.author.name == "srguillermo" and "$copy" in split_msg:
            copy_com_status[0] = 0
            copy_com_target[0] = split_msg[-1]
            print(f"Now copying {copy_com_target[0]}'s messages")
        if copy_com_status[0] == 0 and message.author.name == copy_com_target[-1]:
            await message.channel.send(f"FeelsSpecialMan : {message.content}")

        #Act viewers list
        if message.author.name == "srguillermo" and "$act" in split_msg:
            chatters = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
            chatters.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
            print("Active chatters updated")
    
    
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
                print(f"Namess command used by {ctx.author.name} : {username} ({duration}s {channel})")
            except IndexError:
                await ctx.send(f"/timeout {username} {duration}")
                print(f"Namess command used by {ctx.author.name} : {username} ({duration}s <{ctx.channel.name}>)")
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
                print(f"Nunban command used by {ctx.author.name} : {username} ({channel})")
            except IndexError:
                await ctx.send(f"/unban {username}")
                print(f"Nunban command used by {ctx.author.name} : {username} (<{ctx.channel.name}>)")
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
    
    #Help
    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author.name in AUTHORIZED:
            print("")
    
    #Exceptions            
    @commands.command(aliases=["copystop", "cs", "copy", "act", "ws", "word"])
    async def con(self, ctx: commands.Context):
        pass      


if __name__ == "__main__":
    bot = Bot()  
    bot.run()