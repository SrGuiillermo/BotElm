import requests

cht = requests.get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"]
