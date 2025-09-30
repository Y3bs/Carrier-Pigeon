from code import interact
from socket import timeout
import nextcord
from nextcord.ext import commands
from nextcord.ui import View,Select
from nextcord import Embed, Interaction,SelectOption
from utils.utils import EMOJIES
from cogs.game_modals import Warzone,MarvelRivals

class LoggerDropDown(Select):
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
    async def callback(self, interaction: Interaction):
        selected_item = self.values[0]
        if selected_item == 'warzone':
            await interaction.response.send_modal(Warzone(self.guild_id))
        if selected_item == 'rivals':
            await interaction.response.send_modal(MarvelRivals(self.guild_id))

class Logger(View):
    def __init__(self,guild_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.add_item(LoggerDropDown(self.guild_id))

class Logging(commands.Cog):
    def __init__(self,client):
        self.client = client

    @nextcord.slash_command(name='log_panel',description="sends the panel message for logging accounts")
    async def log_panel(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            error = Embed(
                title='Permissions Error ⛔',
                description="You don't have permission to use to command **(Admins Only 🧑‍💼)**",
                color=0xE80000
            )
            return await interaction.followup.send(embed=error,ephemeral=True)
        channel = interaction.channel
        embed = Embed(
        title ="سجل اكونتك",
        description="دوس علي الزرار اللي تحت عشان تسجل اكونتك الخلصان",
        )
        await channel.send(embed=embed,view=Logger(interaction.guild.id))
        await interaction.followup.send('Panel created ✅',ephemeral=True)

def setup(client):
    client.add_cog(Logging(client))
