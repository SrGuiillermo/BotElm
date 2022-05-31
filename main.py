from twitchio.ext import commands
import random
from asyncio import sleep
from requests import get
import json
import botElm_lib as lib
try:
    with open("confg.json", "r") as f:
        confg = json.load(f)
except FileNotFoundError:
    lib.generate_default_conf()
try:
    with open("clips.json", "r") as f:
        CLIPS = json.load(f)
except FileNotFoundError:
    CLIPS = lib.generate_default_clips()


console_msg_status = [False]
word_list_status = [False]
vanish_com_status = [True]
win_com_status = [False]
samu_com_status = [True]
slot_mach_status = [False]
slot_on_cooldown = [False]
copy_com_status = [False]
copy_com_target = [0]
feiipito_com_status = [True]
feiipito_on_cooldown = [False]
all_commands = [console_msg_status, word_list_status, vanish_com_status, win_com_status, slot_mach_status, \
                copy_com_status, feiipito_com_status, samu_com_status]


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token = confg["tmi"],
            prefix = "$",
            initial_channels = confg["channels"]
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

        #WordList
        if word_list_status[0] == True:
            incl = False
            for i in confg["word_list"]:
                if i in split_msg:
                    incl = True
            if incl == True:
                await sleep(0.3)
                await message.channel.send("/timeout {} {}".format(message.author.name, confg["word_time"]))
            incl = False

        #Copy Command
        if copy_com_status[0] == True:
            if copy_com_target[-1] == message.author.name:
                await message.channel.send(f"FeelsSpecialMan : {message.content}")
        #Samuel Command
        if samu_com_status[0] == True:
            if message.author.name == "samuelvpa":
                if "srguillermo" in message.content.lower() or "@srguillermo" in message.content.lower():
                    await message.channel.send(f"/timeout {message.author.name} 300")

    #Exit
    @commands.command()
    async def exit(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            await ctx.message.channel.send("Close and turn off bot?")
            response = await lib.wait_for_response(self, ctx)
            if response[0] == "y":
                exit()


    #Switches
    #Current Check
    @commands.command()
    async def current(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            print()
            print(f"Console: {console_msg_status[0]} [$con]")
            print(f"Word Command: {word_list_status[0]} [$ws]")
            print(f"Slot Command: {slot_mach_status[0]} [$ss]")
            print(f"Copy Command: {copy_com_status[0]}; Target = {copy_com_target[-1]} [$copy/$cs]")
            print(f"Vanish Command: {vanish_com_status[0]}")
            print(f"Feiipito Command: {feiipito_com_status[0]} [$fs]")
            print(f"Win Command: {win_com_status[0]} [$wins]")
            print(f"Samuel Command: {samu_com_status[0]} [$sams]")
            print()
    #All Off
    @commands.command()
    async def alloff(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.all_off(all_commands, ctx)
    #All On
    @commands.command()
    async def allon(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.all_on(all_commands, ctx)
    #Console Msg
    @commands.command()
    async def con(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(console_msg_status, "Console logs", ctx)
    #Word List
    @commands.command()
    async def ws(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(word_list_status, "Word", ctx)
    #Slot
    @commands.command()
    async def ss(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(slot_mach_status, "Slot machine", ctx)
    #Vanish
    @commands.command()
    async def vs(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(vanish_com_status, "Vanish", ctx)
    #Feiipito
    @commands.command()
    async def fs(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(feiipito_com_status, "Feiipito", ctx)
    #Win
    @commands.command()
    async def wins(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(win_com_status, "Win", ctx)
    #Samuel
    @commands.command()
    async def sams(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(samu_com_status, "Samuel", ctx)
    #CopyStop
    @commands.command(aliases=["copystop"])
    async def cs(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            lib.switch(copy_com_status, "Copy", ctx)
    #CopyTarget
    @commands.command()
    async def copy(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            split_msg = ctx.message.content.split(" ")
            copy_com_status[0] = True
            copy_com_target[0] = split_msg[-1]
            lib.log(f"Now copying {copy_com_target[0]}'s messages")


    #Word
    @commands.command()
    async def word(self, ctx: commands.Context):
        if ctx.author.name in confg["propietary"]:
            split_msg = ctx.message.content.lower().split(" ")
            arg = split_msg[1]
            if arg == "list":
                try:
                    word_time = confg["word_time"]
                    word_all_list = confg["word_list"][0]
                    for i in range(1, len(confg["word_list"])):
                        word_all_list = word_all_list + "," + confg["word_list"][i]
                    print("Currently banning for t = {} the following words: {}".format(confg["word_time"], word_all_list))
                except IndexError:
                    print("Currently not banning any word for t = {}".format(confg["word_time"]))

            if arg == "time":
                try:
                    confg["word_time"] = int(split_msg[-1])
                    lib.json_file_save(file_name="confg.json", dic=confg)
                    lib.log(f"Time in word command changed to {split_msg[-1]} by {ctx.author.name}")
                except ValueError:
                    pass

            if arg == "add":
                for i in range(2, len(split_msg)):
                    if split_msg[i] not in confg["word_list"]:
                        confg["word_list"].append(split_msg[i])
                        lib.log(f"{split_msg[i]} added to word list by {ctx.author.name}")
                lib.json_file_save(file_name="confg.json", dic=confg)
            
            if arg == "remove":
                for i in range(2, len(split_msg)):
                    if split_msg[i] in confg["word_list"]:
                        for a in range(len(confg["word_list"])):
                            if split_msg[i] == confg["word_list"][a]:
                                del confg["word_list"][a]
                                lib.log(f"{split_msg[i]} removed from word list by {ctx.author.name}")
                lib.json_file_save(file_name="confg.json", dic=confg)
            
            if arg == "clean":
                confg["word_list"].clear()
                print(f"Word list cleaned")
                lib.json_file_save(file_name="confg.json", dic=confg)
            
    #Feiipito
    @commands.command()
    async def feiipito(self, ctx: commands.Context):
        if feiipito_com_status[0] == True:
            if feiipito_on_cooldown[0] == False:
                confg["feiipito_count"] += 1
                lib.json_file_save(file_name="confg.json", dic=confg)
                await ctx.send("Feiipito nos ha tocado {} veces PoroSad".format(confg["feiipito_count"]))
                await lib.cooldown(feiipito_on_cooldown, 20)


    #Namess
    @commands.command()
    async def namess(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in confg["authorized"]:
            username = split_msg[1]
            try:
                duration = split_msg[2]
                if int(duration) > 300:
                    duration = 300
                try:
                    channel = self.get_channel(split_msg[3])
                    await channel.send(f"/timeout {username} {duration}")
                    lib.log(f"Namess command used by {ctx.author.name} : {username} ({duration}s {channel})")
                        
                except IndexError:
                    await ctx.send(f"/timeout {username} {duration}")
                    lib.log(f"Namess command used by {ctx.author.name} : {username} ({duration}s <{ctx.channel.name}>)")
                    
            except ValueError:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/timeout {username} 5m")
                lib.log(f"Namess command used by {ctx.author.name} : {username} (5m <{channel}>)")              
            
            except IndexError:
                await ctx.send(f"/timeout {username} 5m")
                lib.log(f"Namess command used by {ctx.author.name} : {username} (5m <{ctx.channel.name}>)")


    #Slot
    @commands.command()
    async def slot(self, ctx: commands.Context):
        if slot_mach_status[0] == True:
            if slot_on_cooldown[0] == False:
                slot_emote = confg["slot"]
                slot_chance = random.randint(1, 4)
                if slot_chance == 2:
                    slot_win = random.randint(0, len(slot_emote) - 1)
                    await ctx.send(f"{ctx.author.name} ㅤ👉 ㅤ[ {slot_emote[slot_win]} | {slot_emote[slot_win]} | {slot_emote[slot_win]} ]ㅤ WIN Pog Esperando un usuario peepoEvil")
                    timeout = await lib.wait_for_response(self, ctx)
                    await ctx.send(f"/timeout {timeout[0]} 60")
                    lib.log(f"Slot command used by {ctx.author.name} : {timeout} <{ctx.channel.name}>")
                else:
                    slot_random = random.sample(range(0, len(slot_emote) - 1), 3)
                    if slot_random[0] == slot_random[1] == slot_random[2]:
                        while slot_random[0] == slot_random[1] == slot_random[2]:
                            slot_random = random.sample(range(0, len(slot_emote) - 1), 3)
                    await ctx.send(f"{ctx.author.name} ㅤ👉 ㅤ[ {slot_emote[slot_random[0]]} | {slot_emote[slot_random[1]]} | {slot_emote[slot_random[2]]} ]ㅤ LOSE -1m PepeGiggle")
                    await ctx.send(f"/timeout {ctx.author.name} 60")
                await lib.cooldown(slot_on_cooldown, 1) 


    #Nunban
    @commands.command()
    async def nunban(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in confg["authorized"]:
            username = split_msg[1]
            try:
                channel = self.get_channel(split_msg[2])
                await channel.send(f"/unban {username}")
                lib.log(f"Nunban command used by {ctx.author.name} : {username} ({channel})")

            except IndexError:
                await ctx.send(f"/unban {username}")
                lib.log(f"Nunban command used by {ctx.author.name} : {username} (<{ctx.channel.name}>)")


    #Linktree spam command
    @commands.command(aliases=["lt"])
    async def linktree(self, ctx: commands.Context):
        split_msg = ctx.message.content.split(" ")
        if ctx.author.name in confg["propietary"]:
            for i in range(int(split_msg[-1])):
                await ctx.send("https://linktr.ee/elmillor Bedge Zzz ")
                await sleep(0.1)


    #Random
    @commands.command(aliases=["gr", "printrandom"])
    async def getrandom(self, ctx: commands.Context):
        CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
        CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])
        await ctx.send(CHATTERS[random.randint(0, len(CHATTERS))])


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
                    if all_clips is None:
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
        if ctx.author.name in confg["admind"]:
            split_msg = ctx.message.content.lower().split(" ")
            if split_msg[1] == "update" or split_msg[1] == "u":
                key = split_msg[2]
                clip = split_msg[3]
                CLIPS.update({key : clip})
                lib.json_file_save(file_name="clips.json", dic=CLIPS)
                await ctx.send(f"Successfully added clip for {key}")
                lib.log(f"{key} clip added by {ctx.author.name}")
            if split_msg[1] == "remove" or split_msg[1] == "r":
                key = split_msg[2]
                await ctx.send(f"Are you sure you want to remove clip for {key}? [Y/N]")
                response = await lib.wait_for_response(self, ctx)
                if response[0] == "y":
                    del CLIPS[key]
                    lib.json_file_save(file_name="clips.json", dic=CLIPS)
                    await ctx.send(f"Successfully removed clip for {key}")
                    lib.log(f"{key} clip removed by {ctx.author.name}")
                else : pass 


    #Help
    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author.name in confg["authorized"]:
            print()
            print("help -- this command")
            print("exit -- exit the bot")
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
            print("sams -- samuel command switch")
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