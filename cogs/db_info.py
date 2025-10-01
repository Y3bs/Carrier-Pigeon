from nextcord.ext import commands
from nextcord import Embed,Interaction,slash_command
import utils.database as db
from datetime import datetime

class Info(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='db_info',description='displays a brief info about the accounts database')
    async def info(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        available_count = db.db.carrier.accounts.count_documents({"available": True})
        taken_count = db.db.carrier.accounts.count_documents({"available": False})
        total_count = available_count + taken_count

        total_bytes = 0
        try:
            for doc in db.db.carrier.accounts.find({}, {"content": 1}):
                content = doc.get("content", "")
                if isinstance(content, str):
                    total_bytes += len(content.encode('utf-8'))
        except Exception:
            total_bytes = 0

        def human_size(n):
            for unit in ["B","KB","MB","GB","TB"]:
                if n < 1024:
                    return f"{n:.0f} {unit}" if unit == "B" else f"{n:.2f} {unit}"
                n /= 1024
            return f"{n:.2f} PB"

        now_utc = datetime.utcnow()
        formatted_time = now_utc.strftime('%d %b %Y, %H:%M:%S UTC')

        embed = Embed(
            title='📊 Accounts Database Info',
            color=0x00ffcc
        )
        embed.add_field(name='🆓 Available', value=str(available_count), inline=True)
        embed.add_field(name='🧧 Taken', value=str(taken_count), inline=True)
        embed.add_field(name='∑ Total', value=str(total_count), inline=True)
        embed.add_field(name='💾 Approx Storage Used', value=human_size(total_bytes), inline=False)
        embed.add_field(name='🕒 Last Update', value=formatted_time, inline=False)

        await interaction.followup.send(embed=embed)

def setup(client):
    client.add_cog(Info(client))