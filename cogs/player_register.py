from enum import member
from nextcord.ext import commands
import utils.database as db
from nextcord import  Interaction, Member,slash_command

class MemberEvent(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='register',description="register your self in the database")
    async def register(self,interaction:Interaction):
        await interaction.response.defer(ephemeral=True)
        uid = interaction.user.id
        db.save_player(uid)
        await interaction.followup.send(f"{interaction.user.mention} is registered in the database")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        uid = member.id
        db.save_player(uid)
    
    @commands.Cog.listener()
    async def on_member_remove(self,member: Member):
        uid = member.id
        db.delete_player(uid)

def setup(client):
    client.add_cog(MemberEvent(client))

    