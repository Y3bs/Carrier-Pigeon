import nextcord
from nextcord import Embed,Message
from nextcord.ext import commands
from datetime import datetime,timezone
import platform

BOT_VERSION = "3.0"
BOT_OWNER = "(⌐■_■)™"
start_time = datetime.now(timezone.utc)

class Version(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self,message: Message):
        if message.author == self.client.user or not message.author.guild_permissions.administrator:
            return  

        if self.client.user.mentioned_in(message):
        
            uptime = datetime.now(timezone.utc) - start_time
            uptime_str = str(uptime).split(".")[0]

            embed = Embed(
                title=f"🤖 {self.client.user.name} Info",
                description="Hey! You mentioned me 👋 Here are my details:",
                color=0x5865F2
            )
            embed.set_thumbnail(url=self.client.user.avatar.url)

            embed.add_field(name="📌 Version", value=BOT_VERSION, inline=True)
            embed.add_field(name="🏓 Ping", value=f"{round(self.client.latency * 1000)} ms", inline=True)
            embed.add_field(name="🌍 Servers", value=f"{len(self.client.guilds)}", inline=True)
            embed.add_field(name="⏳ Uptime", value=uptime_str, inline=True)
            embed.add_field(name="👨‍💻 Developer", value=BOT_OWNER, inline=True)
            embed.set_footer(text=f"Running on Python {platform.python_version()} | Nextcord")

            await message.channel.send(embed=embed)

        await self.client.process_commands(message)

def setup(client):
    client.add_cog(Version(client))