import nextcord
from nextcord.ext import commands
import os 
from cogs.logging import Logger
from cogs.views import MarkSold,Paid
from cogs.fresh import AccRequest
from utils import fresh_manager
from utils.stats_manager import StatsManager
from utils.fresh_manager import FreshManager
from utils.utils import cycle_status
from dotenv import load_dotenv
from utils.database import db

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
TOKEN = os.getenv('TOKEN')

stats_manager = StatsManager('data/stats.json')
fresh_manager = FreshManager()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    # client.loop.create_task(stats_manager.auto_save())
    client.loop.create_task(cycle_status(client))
    client.add_view(Logger(None))
    client.add_view(MarkSold(None))
    client.add_view(Paid(None))
    client.add_view(AccRequest(None))
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    print("🗄️  Database State:")
    print("=" * 50)
    try:
        db.admin.command('ping')
        print("✅ Database Connection: Connected")
    except Exception as e:
        print(f"❌ Database Connection: Failed - {str(e)}")
        print("=" * 50)

client.run(TOKEN)