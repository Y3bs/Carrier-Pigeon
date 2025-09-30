import nextcord 
from nextcord.ext import commands
from nextcord import Embed,Interaction,SelectOption,File,slash_command
from nextcord.ui import View,Select
from utils.fresh_manager import fresh_manager
from utils.utils import EMOJIES

class AccRequestDropDown(Select):
    def __init__(self,guild_id):
        self.guild_id = guild_id
        options = [
            SelectOption(label='Warzone',value='warzone',emoji=EMOJIES['Warzone']),
            SelectOption(label='Marvel Rivals',value='rivals',emoji=EMOJIES['Rivals'])
        ]
        super().__init__(
            placeholder="Select a game...",
            min_values=1,
            max_values=1,
            options=options
        )
    async def callback(self,interaction: Interaction):
        selected = self.values[0]
        await interaction.response.defer(ephemeral=True)
        if selected == 'warzone':
            files = fresh_manager.list_fresh(selected)
            if not files:
                error = Embed(
                    title = 'No Fresh 🪹',
                    description='There is no fresh accounts available for this game for now',
                    color=0xE80000
                )
                return await interaction.followup.send(embed=error,ephemeral=True)
            embed = Embed(
                title = 'Fresh Sent Successfully ✅',
                description='الفريش اتبعتلك في ال dm.\nHave Fun 😊',
                color = 0x038c07
            )
            acc = fresh_manager.get_first_fresh(selected)
            await interaction.user.send(f"اوعي الفريش 🧃:\n",file = File(acc))
            await interaction.followup.send(embed = embed,ephemeral=True)
            fresh_manager.move_to_taken(str(interaction.user.name),selected)
            
        if selected == 'rivals':
            await interaction.followup.send('لسه مشغلتهاش شوفلك لعبة تانية لحد ما تشتغل',ephemeral=True)


class AccRequest(View):
    def __init__(self,guild_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.add_item(AccRequestDropDown(self.guild_id))

class Fresh(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='fresh_panel',description='Sends the panel for fresh accounts')
    async def fresh_panel(self,interaction:Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(
        title='الفريش 🧃',
        description='اختار اللعبة اللي عايز منها الفريش'
        )
        await interaction.channel.send(embed=embed,view=AccRequest(interaction.guild.id))
        await interaction.followup.send('Panel Created ✅',ephemeral=True)


def setup(client):
    client.add_cog(Fresh(client))