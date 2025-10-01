import nextcord
from nextcord.ext import commands
from nextcord import Interaction,Embed
import utils.database as db

class Stats(commands.Cog):
    def __init__(self,client):
        self.client = client

    @nextcord.slash_command(name='me',description="shows your earnings, number of banned,sold accounts")
    async def stats(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        uid = interaction.user.id
        user_stats = db.find_player(uid)
        success_rate = db.success_rate(uid)
        avg_sale = db.avg_sale(uid)

        embed = Embed(
            description=f'# 📊 Stats for {interaction.user.mention}',
            color=0x00E6E6
        )
        embed.add_field(name='💸 Sold',value=f'{user_stats['sold']} Account')
        embed.add_field(name='⛔ Banned',value=f'{user_stats['banned']} Account')
        embed.add_field(name='📦 Success Rate',value=f'{success_rate}%')
        embed.add_field(name='💰 Total Earnings',value=f'{user_stats['earnings']} L.E')
        embed.add_field(name='⚖️ Avg. Sale Price',value=f'{avg_sale} L.E')
        embed.add_field(name='💳 Wallets',value=f'{len(user_stats['wallets'])}')

        await interaction.followup.send(embed=embed,ephemeral=True)

def setup(client):
    client.add_cog(Stats(client))