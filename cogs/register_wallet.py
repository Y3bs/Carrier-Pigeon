import nextcord
from nextcord.ext import commands
from nextcord import Embed, Interaction, SelectOption
from nextcord.ui import View,Select
from utils.stats_manager import stats_manager
from utils.utils import EMOJIES
from cogs.wallet_modals import Vodafone,Instapay,Visa

class WalletTypeDropDown(Select):
    def __init__(self):
        options = [
            SelectOption(label='Vodafone Cash',value='vodafone',emoji=EMOJIES['vodafone']),
            SelectOption(label='Instapay',value='instapay',emoji=EMOJIES['instapay']),
            SelectOption(label='Visa',value='visa',emoji=EMOJIES['visa'])
        ]
        
        super().__init__(
            placeholder='Select a wallet type',
            min_values=1,
            max_values=1,
            options=options
        )
    async def callback(self, interaction: Interaction):
        selected = self.values[0]
        if selected == 'vodafone':
            await interaction.response.send_modal(Vodafone())
        if selected == 'instapay':
            await interaction.response.send_modal(Instapay())
        if selected == 'visa':
            await interaction.response.send_modal(Visa())


class WalletType(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(WalletTypeDropDown())
    

class Wallet(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @nextcord.slash_command(name='register_wallet',description='save ur payment addresse for ez access later')
    async def register_wallet(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(
            title='Choose your wallet type',
            description=f'Supported types',
            color=0x040dbf
        )
        embed.add_field(name=f'{EMOJIES['vodafone']} Vodafone Cash',value=' ')
        embed.add_field(name=f'{EMOJIES['instapay']} Instapay',value=' ')
        embed.add_field(name=f'{EMOJIES['visa']} Visa',value=' ')
        await interaction.followup.send(embed=embed,view=WalletType(),ephemeral=True)

def setup(client):
    client.add_cog(Wallet(client))