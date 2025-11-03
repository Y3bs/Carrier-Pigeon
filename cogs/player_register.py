from nextcord.ext import commands
import utils.database as db
from nextcord import  Interaction, slash_command, Embed

class MemberEvent(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='register',description="register your self in the database")
    async def register(self,interaction:Interaction):
        await interaction.response.defer(ephemeral=True)
        if not interaction.guild:
            error = Embed(
                title = 'Guild Error ⛔',
                description='This command can only run in:\n> Servers',
                color = 0xE80000
            )
            return await interaction.followup.send(embed=error , ephemeral=True)
        uid = interaction.user.id
        if db.find_player(uid):
            return await interaction.followup.send(f"You already exist in the database")
        db.save_player(uid)
        await interaction.followup.send(f"{interaction.user.mention} is registered in the database")

def setup(client):
    client.add_cog(MemberEvent(client))

    