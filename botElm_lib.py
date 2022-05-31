from twitchio.ext import commands
import json
import asyncio
import time

def json_file_save(file_name, dic):
    with open(file_name, "w") as f:
        json.dump(dic, f)
        
def switch(command_status, command_name, ctx: commands.Context):
    if command_status[0] == True:
        command_status[0] = False
        log(f"{command_name} command turned off by {ctx.author.name}")
    elif command_status[0] == False:
        command_status[0] = True
        log(f"{command_name} command turned on by {ctx.author.name}")

def generate_default_conf():
    temp = {
        "tmi" : "",
        "channels" : [""],
        "authorized" : [""],
        "propietary" : [""],
        "slot" : [""],
        "feiipito_count" : 0,
        "word_list" : [],
        "word_time" : 300
        }
    with open("confg.json", "w") as f:
        json.dump(temp, f)
    print(".json config file created. Please enter values on config.json file before use")
    input()
    exit()

def generate_default_clips():
    temp = {
        "last" : ""
    }
    with open("clips.json", "w") as f:
        json.dump(temp, f)
    return temp

def all_on(all_commands, ctx: commands.Context):
    for i in all_commands:
        i[0] = True
    log(f"All commands turned on by {ctx.author.name}")

def all_off(all_commands, ctx: commands.Context):
    for i in all_commands:
        i[0] = False
    log(f"All commands turned off by {ctx.author.name}")

async def cooldown(command_on_cooldown, cooldown):
    command_on_cooldown[0] = True
    await asyncio.sleep(cooldown)
    command_on_cooldown[0] = False

async def wait_for_response(self, ctx: commands.Context):
    original_au = ctx.author.name
    while True:
        message = await self.wait_for("message")
        try:
            author = message[0].author.name
            if author == original_au:
                response = message[0].content.lower().split(" ")
                break
        except AttributeError:
            pass
    return response


def log(log_to_save):
    log = (f"{time.localtime().tm_hour}:{time.localtime().tm_min} [{time.localtime().tm_mday}/{time.localtime().tm_mon}]\t"\
           f"{log_to_save}")
    print(log)
    with open("logs.txt", "a") as f:
        f.write(f"{log}\n")
"""
------------------------------------------------------------------------
if split_msg[0] == "livee":
    a = await self.fetch_streams(user_logins=["elmiillor"])
    print(a)
------------------------------------------------------------------------
@commands.command()
@commands.cooldown(1, 1)
async def belvin(self, ctx: commands.Context):
    try:
        if ctx.author.badges["vip"] == "1":
            await ctx.send(f"/timeout belvinxd 60")
    except KeyError: pass
-------------------------------------------------------------------------
"""