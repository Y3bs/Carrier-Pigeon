import nextcord 
from nextcord import Embed,Activity,Game,ActivityType,Message
from itertools import cycle 
import asyncio
import re

EMOJIES = {
    'Rivals': '<:MarvelRivals:1409200032510378066>',
    'Warzone': '<:Warzone:1409198964774801478>',
    'vodafone': '<:Vodafone:1415360491697733828>',
    'instapay': '<:Instapay:1415360732232421378>',
    'visa': '<:Visa:1415361170222616687>',
}

async def move_channel(channel,category_name,emoji,color,title,desc):
    guild = channel.guild
    category = nextcord.utils.get(guild.categories,name=category_name)
    if category is None:
        category = await guild.create_category(category_name)
    await channel.edit(name=f'{emoji}{channel.name[1:]}',category=category)
    return Embed(title=title,description=desc,color=color)

statuses = cycle([
    Game("💸 Selling accounts"),
    Activity(type=ActivityType.listening, name="customers"),
    Activity(type=ActivityType.watching, name="📦 Orders come & go"),
    Game("⛔ Handling bans"),
    Activity(type=ActivityType.watching, name="earnings grow 💰"),
    Activity(type=ActivityType.listening,name='Auto saving files 🗃️'),
    Game("v4.0")
])

async def cycle_status(client, interval=60):
    """Loop through statuses every X seconds (default 60)."""
    while True:
        await client.change_presence(activity=next(statuses))
        await asyncio.sleep(interval)

def get_user_id(msg: Message):
    id = re.search(r"<@!?(\d+)>", msg.content)
    if id:
        return int(id.group(1))
    return None

def check_wallet_type(select:str,type: str):
    if select == 'vodafone':
        num = '0125'
        if not type.startswith('01') or type[2] not in num or not type[3:].isdigit():
            return False
    if select == 'instapay':
        if not type.endswith('@instapay'):
            return False
    if select == 'visa':
        if not type.isdigit():
            return False
        total = 0
        reverse = type[::-1]

        for i,digit in enumerate(reverse):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -=9
            total += n
        return total % 10 == 0
    return True

def setup(client):
    pass