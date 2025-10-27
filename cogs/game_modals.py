import nextcord
from nextcord import TextInputStyle,Interaction,Embed,PermissionOverwrite
from nextcord.ui import Modal,TextInput
from cogs.views import MarkSold

class Warzone(Modal):
    def __init__(self, guild_id):
        super().__init__(title="Account Details")
        self.guild_id = guild_id
        self.add_item(TextInput(label="Level",style=TextInputStyle.short,placeholder="حط لفل الاكونت",required=True))
        self.add_item(TextInput(label="Ready Rank?",style=TextInputStyle.short,placeholder='حط كلمه rfr',required=True))
        self.add_item(TextInput(label="Maxed Guns",style=TextInputStyle.short,placeholder='حط عدد الاسلحة الماكس مش اسمائهم',required=True))
    async def callback(self, interaction: Interaction):
        level = self.children[0].value
        rank = self.children[1].value
        guns = self.children[2].value
        guild = interaction.guild

        category = nextcord.utils.get(guild.categories, name="For Sale 🏷️")
        if category is None:
            category = await guild.create_category("For Sale 🏷️")

        rank = 'rfr' if rank.lower() == 'rfr' else None
        account_name = f'wz-{level}-{rank}-{guns}-max'

        user = interaction.user
        guild = interaction.guild
        everyone = guild.default_role
        overwrites = {
            everyone: PermissionOverwrite(view_channel=False),
            user: PermissionOverwrite(view_channel=True,send_messages=True)
        }
        channel = await category.create_text_channel(f"🏷️{account_name}",overwrites=overwrites)
        embed = Embed(
            title='تأكيد التسليم',
            description='دوس علي الزار اللي تحت عشان تأكد ان الاكونت اتسلم لحد',
            color = 0x040dbf
        )
        confirm_embed = Embed(
            title='✅ Channel created successfully',
            description=f'Your channel\n# {channel.mention}',
            color=0x038c07
        )
        await interaction.response.send_message(embed=confirm_embed,ephemeral=True)
        msg = await channel.send(content=interaction.user.mention,embed=embed, view=MarkSold(self.guild_id))
        await msg.pin()

class MarvelRivals(Modal):
    def __init__(self,guild_id):
        super().__init__(title="Account Details")
        self.guild_id = guild_id
        self.add_item(TextInput(label='Account Rank/Level',placeholder='حط رانك او لفل الاكونت علي حسب',required=True))
    async def callback(self, interaction: Interaction):
        detail = self.children[0].value
        guild = interaction.guild
        category = nextcord.utils.get(guild.categories, name="For Sale 🏷️")
        if category is None:
            category = await guild.create_category("For Sale 🏷️")
        account_name = f'rivals-{detail}'

        user = interaction.user
        guild = interaction.guild
        everyone = guild.default_role
        overwrites = {
            everyone: nextcord.PermissionOverwrite(view_channel=False),
            user: nextcord.PermissionOverwrite(view_channel=True,send_messages=True)
        }
        channel = await category.create_text_channel(f'🏷️{account_name}',overwrites=overwrites)
        embed = Embed(
            title='تأكيد التسليم',
            description='دوس علي الزار اللي تحت عشان تأكد ان الاكونت اتسلم لحد',
            color = 0x040dbf
        )
        confirm_embed = Embed(
            title='✅ Channel created successfully',
            description=f'Your channel\n# {channel.mention}',
            color=0x038c07
        )
        await interaction.response.send_message(embed=confirm_embed,ephemeral=True)
        msg = await channel.send(content=interaction.user.mention,embed=embed, view=MarkSold(self.guild_id))
        await msg.pin()

def setup(client):
    pass