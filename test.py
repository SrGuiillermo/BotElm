from random import randint
from requests import get

CHATTERS = get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["vips"]
CHATTERS.extend(get("https://tmi.twitch.tv/group/user/elmiillor/chatters").json()["chatters"]["viewers"])

print(CHATTERS)