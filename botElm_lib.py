from twitchio.ext import commands
import json
import asyncio
from logging import info, debug


def json_file_save(file_name, dic):
    with open(file_name, "w") as f:
        json.dump(dic, f)
        
def switch(command_status, command_name):
    if command_status[0] == True:
        command_status[0] = False
        info(f"{command_name} command turned off")
    elif command_status[0] == False:
        command_status[0] = True
        info(f"{command_name} command turned on")

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
    debug(".json config file created. Please enter values on config.json file before use")
    input()
    exit()

def generate_default_clips():
    temp = {
        "last" : ""
    }
    with open("clips.json", "w") as f:
        json.dump(temp, f)
    return temp

def all_on(all_commands):
    for i in all_commands:
        i[0] = True
    info("All commands turned on")

def all_off(all_commands):
    for i in all_commands:
        i[0] = False
    info("All commands turned off")

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