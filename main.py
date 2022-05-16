from twitchio.ext import commands
import random
from asyncio import sleep
from requests import get
import json
import time
try:
    with open("confg.json", "r") as f:
        confg = json.load(f)
except FileNotFoundError:
    temp = {
        "tmi" : "",
        "channels" : [""],
        "authorized" : [""],
        "propietary" : [""],
        "slot" : [""],
        "feiipito_count" : 0
        }
    with open("confg.json", "w") as f:
        json.dump(temp, f)
    print(".json config file created. Please enter values on config.json file before use")
    input()
    exit()
try:
    with open("clips.json", "r") as f:
        CLIPS = json.load(f)
except FileNotFoundError:
    temp = {
        "last" : ""
    }
    with open("clips.json", "w") as f:
        json.dump(temp, f)
    CLIPS = temp


TOKEN = confg["tmi"]
CHANNELS = confg["channels"]
AUTHORIZED = confg["authorized"]
ADMIND = confg["admind"]
PROPIETARY = confg["propietary"]
SLOT_EMOTE = confg["slot"]
CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])

"""try:
    WORD_LIST = open("word_list.txt", "r").read().split(",")
except FileNotFoundError:
    temp = ["3600"]
    with open("word_list.txt", "w") as f:
        f.writelines(temp)
    WORD_LIST = temp"""


console_msg_status = [False]
word_list_status = [False]
vanish_com_status = [True]
win_com_status = [True]
slot_mach_status = [False]
slot_on_cooldown = [False]
copy_com_status = [False]
copy_com_target = [0]
feiipito_com_status = [True]
feiipito_on_cooldown = [False]


def confg_file_save():
    with open("confg.json", "w") as f:
        json.dump(confg, f)
def clips_file_save():
    with open("clips.json", "w") as f:
        json.dump(CLIPS, f)
def switch(command_status, command_name):
    if command_status[0] == True:
        command_status[0] = False
        print(f"{command_name} command turned off")
    elif command_status[0] == False:
        command_status[0] = True
        print(f"{command_name} command turned on")


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

        """if split_msg[0] == "livee":
            a = await self.fetch_streams(user_logins=["elmiillor"])
            print(a)"""

        #WordList
        if word_list_status[0] == True:
            incl = False
            for i in confg["word_list"]:
                if i in split_msg:
                    incl = True
            if incl == True:
                await sleep(0.3)
                word_time = confg["word_time"]
                await message.channel.send(f"/timeout {message.author.name} {word_time}")
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
            feiipito_com_status[0] = False
            win_com_status[0] = False
            print("All commands turned off")
    #All On
    @commands.command()
    async def allon(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            console_msg_status[0] = True
            word_list_status[0] = True
            slot_mach_status[0] = True
            vanish_com_status[0] = True
            feiipito_com_status[0] = True
            win_com_status[0] = True
            print("All commands turned on")
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
            print(f"Win Command: {win_com_status[0]} [$wins]")
            print()
    #Console Msg
    @commands.command()
    async def con(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            if console_msg_status[0] == False:
                console_msg_status[0] = True
                print("Console logs turned on")
            elif console_msg_status[0] == True:
                console_msg_status[0] = False
                print("Console logs turned off")
    #Word List
    @commands.command()
    async def ws(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            switch(word_list_status, "Word")
    #Slot
    @commands.command()
    async def ss(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            switch(slot_mach_status, "Slot machine")
    #Vanish
    @commands.command()
    async def vs(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            switch(vanish_com_status, "Vanish")
    #Feiipito
    @commands.command()
    async def fs(self, ctx: commands.Context):
        if ctx.author.name in PROPIETARY:
            switch(feiipito_com_status, "Feiipito")
    #Win
    @commands.command()
    async def wins(self, ctx: commands.Context):
        switch(win_com_status, "Win")
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
                try:
                    word_time = confg["word_time"]
                    word_all_list = confg["word_list"][0]
                    for i in range(1, len(confg["word_list"])):
                        word_all_list = word_all_list + "," + confg["word_list"][i]
                    print(f"Currently banning for t = {word_time} the following words: {word_all_list}")
                except IndexError:
                    print(f"Currently not banning any word for t = {word_time}")

            if split_msg[1] == "time":
                try:
                    confg["word_time"] = int(split_msg[-1])
                    confg_file_save()
                    print(f"Time in word command changed to {split_msg[-1]}")
                except ValueError:
                    pass

            if split_msg[1] == "add":
                for i in range(2, len(split_msg)):
                    if split_msg[i] not in confg["word_list"]:
                        confg["word_list"].append(split_msg[i])
                        print(f"{split_msg[i]} added to word list")
                confg_file_save()
            
            if split_msg[1] == "remove":
                for i in range(2, len(split_msg)):
                    if split_msg[i] in confg["word_list"]:
                        for a in range(len(confg["word_list"])):
                            if split_msg[i] == confg["word_list"][a]:
                                del confg["word_list"][a]
                                print(f"{split_msg[i]} removed from word list")
                confg_file_save()
            
            if split_msg[1] == "clean":
                confg["word_list"].clear()
                print(f"Word list cleaned")
                confg_file_save()
            
    #Feiipito
    @commands.command()
    async def feiipito(self, ctx: commands.Context):
        if feiipito_com_status[0] == True and feiipito_on_cooldown[0] == False:
            confg["feiipito_count"] += 1
            confg_file_save()
            count = confg["feiipito_count"]
            await ctx.send(f"Feiipito nos ha tocado {count} veces PoroSad")
            feiipito_on_cooldown[0] = True
            await sleep(40)
            feiipito_on_cooldown[0] = False


    #Namess
    @commands.command()
    async def namess(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[1]
            try:
                duration = split_msg[2]
                if int(duration) > 300:
                    duration = 300
                try:
                    channel = self.get_channel(split_msg[3])
                    await channel.send(f"/timeout {username} {duration}")
                    print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]ㅤ"\
                        f"Namess command used by {ctx.author.name} : {username} ({duration}s {channel})")
                except IndexError:
                    await ctx.send(f"/timeout {username} {duration}")
                    print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]ㅤ"\
                        f"Namess command used by {ctx.author.name} : {username} ({duration}s <{ctx.channel.name}>)")
            except ValueError:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/timeout {username} 5m")                
            except IndexError:
                await ctx.send(f"/timeout {username} 5m")


    #Slot
    @commands.command()
    async def slot(self, ctx: commands.Context):
        if slot_mach_status[0] == True and slot_on_cooldown[0] == False:
            slot_emote = SLOT_EMOTE
            slot_chance = random.randint(1, 4)
            if slot_chance == 2:
                slot_win = random.randint(0, len(slot_emote) - 1)
                await ctx.send(f"{ctx.author.name} ㅤ👉 ㅤ[ {slot_emote[slot_win]} | {slot_emote[slot_win]} | {slot_emote[slot_win]} ]ㅤ WIN Pog Esperando un usuario peepoEvil")
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
                await ctx.send(f"{ctx.author.name} ㅤ👉 ㅤ[ {slot_emote[slot_random[0]]} | {slot_emote[slot_random[1]]} | {slot_emote[slot_random[2]]} ]ㅤ LOSE -1m PepeGiggle")
                await ctx.send(f"/timeout {ctx.author.name} 60")
            slot_on_cooldown[0] = True
            await sleep(1)
            slot_on_cooldown[0] = False    


    #Nunban
    @commands.command()
    async def nunban(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in AUTHORIZED:
            username = split_msg[1]
            try:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/unban {username}")
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]ㅤ"\
                    f"Nunban command used by {ctx.author.name} : {username} ({channel})")
            except IndexError:
                await ctx.send(f"/unban {username}")
                print(f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]ㅤ"\
                    f"Nunban command used by {ctx.author.name} : {username} (<{ctx.channel.name}>)")


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
        CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
        CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
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


    #Clips
    @commands.command()
    async def win(self, ctx: commands.Context):
        if win_com_status[0] == True:
            split_msg = ctx.message.content.lower().split(" ")
            clip = split_msg[1]
            if clip == "clips":
                all_clips = None
                for i in CLIPS:
                    if all_clips == None:
                        all_clips = i
                    else:
                        all_clips = all_clips + " / " + i
                await ctx.send(f"All clips avaliable: {all_clips}")
            else:
                try:
                    await ctx.send(CLIPS[clip])
                except KeyError:
                    await ctx.send('Clip not found, use "$win clips" if you want to see all clips avaliable')
    
    
    #Clips admind command
    @commands.command()
    async def clip(self, ctx: commands.Context):
        if ctx.author.name in ADMIND:
            split_msg = ctx.message.content.lower().split(" ")
            if split_msg[1] == "update" or split_msg[1] == "u":
                key = split_msg[2]
                clip = split_msg[3]
                CLIPS.update({key : clip})
                clips_file_save()
                await ctx.send(f"Successfully added clip for {key}")
            if split_msg[1] == "remove" or split_msg[1] == "r":
                key = split_msg[2]
                original_au = ctx.author.name
                await ctx.send(f"Are you sure you want to remove clip for {key}? [Y/N]")
                while True:
                    message = await self.wait_for("message")
                    try:
                        author = message[0].author.name
                        if author == original_au:
                            response = message[0].content.lower().split(" ")
                            if response[0] == "y":
                                del CLIPS[key]
                                clips_file_save()
                                await ctx.send(f"Successfully removed clip for {key}")
                                break
                            else:
                                break
                    except AttributeError:
                        pass



    #Help
    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author.name in AUTHORIZED:
            print()
            print("help -- this command")
            print("v -- self 1 sec timeout")
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
            print("current -- current status of all commands")
            print("slot -- slot command")
            print("feiipito -- feiipito count")
            print("win -- clips public command")
            print("clip -- clip admind command")
            print()     


if __name__ == "__main__":
    bot = Bot()  
    bot.run()