from nextcord.ext import commands
from nextcord import Embed,Interaction,slash_command
from utils.fresh_manager import fresh_manager as fm
class Info(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='db_info',description='displays a brief info about the accounts database')
    async def info(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        fresh = len(fm.list_fresh('warzone'))
        taken = len(fm.list_taken('warzone'))

        embed = Embed(
            title = '📊 Data Base Info',
            color=0x00ffcc
        )
        embed.add_field(name='🆓 Available Accounts',value=fresh)
        embed.add_field(name='🧧 Taken Accounts',value=taken)
        embed.add_field(name='💾 Storage', value='Unlimited')

        await interaction.followup.send(embed=embed)

def setup(client):
    client.add_cog(Info(client))