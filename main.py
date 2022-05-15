from twitchio.ext import commands
import random
from asyncio import sleep
from requests import get
import json
import time
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    temp = {
        "tmi" : "",
        "channels" : [""],
        "authorized" : [""],
        "propietary" : [""],
        "slot" : [""],
        "feiipito" : 0
        }
    with open("config.json", "w") as f:
        json.dump(temp, f)
    print(".json config file created. Please enter values on config.json file before use")
    input()
    exit()


TOKEN = config["tmi"]
CHANNELS = config["channels"]
AUTHORIZED = config["authorized"]
PROPIETARY = config["propietary"]
SLOT_EMOTE = config["slot"]
CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
try:
    WORD_LIST = open("word_list.txt", "r").read().split(",")
except FileNotFoundError:
    temp = ["3600"]
    with open("word_list.txt", "w") as f:
        f.writelines(temp)
    WORD_LIST = temp

slot_mach_status = [False]
console_msg_status = [False]
word_list_status = [False]
copy_com_status = [False]
copy_com_target = [0]
vanish_com_status = [True]
feiipito_com_status = [True]


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token = TOKEN,
            prefix = "$",
            initial_channels = CHANNELS
            )
        print("BOT READY")

    async def event_message(self, message):
        split_msg = message.content.lower().split(" ")

        #Console msg
        if message.echo:
            return
        if console_msg_status[0] == True:
            print(f"<{message.channel.name}> {message.author.name} : {message.content}")
        await self.handle_commands(message)


        #WordList Use
        if word_list_status[0] == True:
            incl = False
            for i in range(1, len(WORD_LIST)):
                if WORD_LIST[i] in split_msg:
                    incl = True
            if incl == True:
                await sleep(0.8)
                await message.channel.send(f"/timeout {message.author.name} {WORD_LIST[0]}")
            incl = False

        #Copy Command
        if copy_com_status[0] == True and copy_com_target[-1] == message.author.name:
                await message.channel.send(f"FeelsSpecialMan : {message.content}")


    #Switches
    #All Off
    @commands.command()
    async def alloff(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            console_msg_status[0] = False
            word_list_status[0] = False
            slot_mach_status[0] = False
            copy_com_status[0] = False
            vanish_com_status[0] = False
    #All On
    @commands.command()
    async def allon(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            console_msg_status[0] = True
            word_list_status[0] = True
            slot_mach_status[0] = True
            vanish_com_status[0] = True
    #Current Check
    @commands.command()
    async def current(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            print()
            print(f"Console: {console_msg_status[0]} [$con]")
            print(f"Word Command: {word_list_status[0]} [$ws]")
            print(f"Slot Command: {slot_mach_status[0]} [$ss]")
            print(f"Copy Command: {copy_com_status[0]}; Target = {copy_com_target[-1]} [$copy/$cs]")
            print(f"Vanish Command: {vanish_com_status[0]}")
            print(f"Feiipito Command: {feiipito_com_status[0]} [$fs]")
            print()
    #Console Msg
    @commands.command()
    async def con(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if console_msg_status[0] == False:
                console_msg_status[0] = True
            elif console_msg_status[0] == True:
                console_msg_status[0] = False
    #Word List
    @commands.command()
    async def ws(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if word_list_status[0] == False:
                word_list_status[0] = True
            elif word_list_status[0] == True:
                word_list_status[0] = False
    #Slot
    @commands.command()
    async def ss(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if slot_mach_status[0] == False:
                slot_mach_status[0] = True
            elif slot_mach_status[0] == True:
                slot_mach_status[0] = False
    #Vanish
    @commands.command()
    async def vs(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if vanish_com_status[0] == True:
                vanish_com_status[0] = False
            elif vanish_com_status[0] == False:
                vanish_com_status[0] = True
    #Feiipito
    @commands.command()
    async def fs(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if feiipito_com_status[0] == True:
                feiipito_com_status[0] = False
            elif feiipito_com_status[0] == False:
                feiipito_com_status[0] = True
    #ChattersList
    @commands.command()
    async def act(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
            CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
            print("Active chatters updated")
    #CopyStop
    @commands.command(aliases=["copystop"])
    async def cs(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            copy_com_status[0] = False
            print("Copy command stopped")
    #CopyTarget
    @commands.command()
    async def copy(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            split_msg = ctx.message.content.split(" ")
            copy_com_status[0] = True
            copy_com_target[0] = split_msg[-1]
            print(f"Now copying {copy_com_target[0]}'s messages")


    #Word
    @commands.command()
    async def word(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            split_msg = ctx.message.content.lower().split(" ")

            if split_msg[1] == "list":
                print(f"Currently banning for t:{WORD_LIST[0]} to following words: {WORD_LIST}")

            if split_msg[1] == "time":
                WORD_LIST[0] = split_msg[-1]
                with open("word_list.txt", "w") as f:
                    f.write(",".join(WORD_LIST))
                print(f"Time in word command changed to {split_msg[-1]}")

            if split_msg[1] == "add":
                for i in range(2, len(split_msg)):
                    if split_msg[i] not in WORD_LIST:
                        WORD_LIST.append(split_msg[i])
                        print(f"{split_msg[i]} added to word list")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(WORD_LIST))
            
            if split_msg[1] == "remove":
                for i in range(2, len(split_msg)):
                    if split_msg[i] in WORD_LIST:
                        for a in range(len(WORD_LIST)):
                            if split_msg[i] == WORD_LIST[a]:
                                del WORD_LIST[a]
                                print(f"{WORD_LIST[a]} removed from word list")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(WORD_LIST))
            
            if split_msg[1] == "clean":
                for i in range(1, len(WORD_LIST)):
                    del WORD_LIST[i]
                    print(f"Word list cleaned")
                with open("word_list.txt", "w") as f:
                    f.write(",".join(WORD_LIST))
            
    #Feiipito
    @commands.command()
    async def feiipito(self, ctx: commands.Context):
        if feiipito_com_status[0] == True:
            config["feiipito"] += 1
            with open("config.json", "w") as f:
                json.dump(config, f)
            count = config["feiipito"]
            await ctx.send(f"Feiipito nos ha tocado {count} veces PoroSad")


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
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]")
                print(f"Namess command used by {ctx.author.name} : {username} ({duration}s {channel})")
            except IndexError:
                await ctx.send(f"/timeout {username} {duration}")
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]")
                print(f"Namess command used by {ctx.author.name} : {username} ({duration}s <{ctx.channel.name}>)")


    #Slot
    @commands.command()
    @commands.cooldown(1, 1, commands.cooldowns.Bucket.user)
    async def slot(self, ctx: commands.Context):
        if slot_mach_status[0] == True:
            slot_emote = SLOT_EMOTE
            slot_chance = random.randint(1, 4)
            if slot_chance == 2:
                slot_win = random.randint(0, len(slot_emote) - 1)
                await ctx.send(f"[ {slot_emote[slot_win]} | {slot_emote[slot_win]} | {slot_emote[slot_win]} ] WIN Pog")
                await ctx.send("Esperando usuario")
                original_au = ctx.author.name
                while True:
                    message = await self.wait_for("message")
                    try:
                        author = message[0].author.name
                        if author == original_au:
                            timeout = message[0].content.lower().split(" ")
                            await ctx.send(f"/timeout {timeout[0]} 60")
                            break
                    except AttributeError:
                        pass
            else:
                slot_random = random.sample(range(0, len(slot_emote) - 1), 3)
                if slot_random[0] == slot_random[1] == slot_random[2]:
                    while slot_random[0] == slot_random[1] == slot_random[2]:
                        slot_random = random.sample(range(0, len(slot_emote) - 1), 3)
                await ctx.send(f"[ {slot_emote[slot_random[0]]} | {slot_emote[slot_random[1]]} | {slot_emote[slot_random[2]]} ] LOSE")
                await sleep(0.5)
                await ctx.send(f"/timeout {ctx.author.name} 60")         


    #Nunban
    @commands.command()
    async def nunban(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[1]
            try:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/unban {username}")
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]")
                print(f"Nunban command used by {ctx.author.name} : {username} ({channel})")
            except IndexError:
                await ctx.send(f"/unban {username}")
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]")
                print(f"Nunban command used by {ctx.author.name} : {username} (<{ctx.channel.name}>)")


    #Linktree spam command
    @commands.command(aliases=["lt"])
    async def linktree(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in PROPIETARY:
            for i in range(int(split_msg[-1])):
                await self.get_channel("ElmiilloR").send("https://linktr.ee/elmillor Bedge Zzz ")
                await sleep(0.1)


    #Random
    @commands.command(aliases=["gr", "printrandom"])
    async def getrandom(self, ctx: commands.Context):
        await ctx.send(CHATTERS[random.randint(0, len(CHATTERS))])
    
    
    """ 
    @commands.command()
    @commands.cooldown(1, 1)
    async def belvin(self, ctx: commands.Context):
        try:
            if ctx.author.badges["vip"] == "1":
                await ctx.send(f"/timeout belvinxd 60")
        except KeyError: pass
    """


    #Vanish Command
    @commands.command()
    async def v(self, ctx: commands.Context):
        if vanish_com_status[0] == True:
            await ctx.send(f"/timeout {ctx.author.name} 1")


    #Help
    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author.name in AUTHORIZED:

            print()
            print("help -- this command")
            print("v -- self 1 sec timeout")
            print("act -- update viewer list")
            print("getrandom / gr / printrandom -- send random viewer")
            print("linktree / lt -- linktree spam")
            print("namess -- ban [user]")
            print("nunban -- unban [user]")
            print("copy -- start copy [user]")
            print("cs -- stop copy command")
            print("word -- word list ban [list/time/add/remove/clean]")
            print("ws -- word command switch")
            print("con -- console log switch")
            print("ss -- slots command switch")
            print("alloff -- shut down all commands")
            print("allon -- actiate all commands")
            print("status -- current status of all commands")
            print("slot -- slot command")
            print()     


if __name__ == "__main__":
    bot = Bot()  
    bot.run()