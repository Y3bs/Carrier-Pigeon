from nextcord import ButtonStyle,Button,Interaction
from nextcord.ui import View,Button,Modal,TextInput,button
from utils.stats_manager import stats_manager
from utils.utils import EMOJIES, move_channel,get_user_id

class MarkSold(View):
    def __init__(self,guild_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id

    @button(
        label='سلمت الاكونت',
        custom_id='sold',
        style=ButtonStyle.blurple,
        emoji="📦"
    )

    async def mark_sold(self,button:Button,interaction:Interaction):
        msg = interaction.message
        channel = interaction.channel
        category_name = "Sold 📦"
        emoji = "📦"
        color = 0x038c07
        title = "الكاش 💰"
        desc = 'دوس علي الزرار اللي تحت لما فلوس الاكونت توصلك'
        uid = get_user_id(msg)
        data = stats_manager.get_user(uid)
        embed = await move_channel(channel,category_name,emoji,color,title,desc)

        visa_data = data["wallets"].get("visa", [])

        if visa_data:
            visa = "\n".join(
                [f"💳 {card['holder name']} — {card['number']}" for card in visa_data]
            )
        else:
            visa = None

        vodafone_data = data["wallets"].get("vodafone", [])

        if vodafone_data:
            vodafone = "\n".join([f"📱 {num}" for num in vodafone_data])
        else:
            vodafone = None

        instapay_data = data["wallets"].get("instapay", [])

        if instapay_data:
            instapay = "\n".join([f"🆔 {num}" for num in instapay_data])
        else:
            instapay = None

        if vodafone:
            embed.add_field(name=f'{EMOJIES['vodafone']} Vodafone Cash Numbers',value=f'```{vodafone}```',inline=False)
        if visa:
            embed.add_field(name=f'{EMOJIES['visa']} Visa Cards',value=f'```{visa}```',inline=False)
        if instapay:
            embed.add_field(name=f'{EMOJIES['instapay']} Instapay Addresses',value=f'```{instapay}```',inline=False)

        await msg.edit(content=f'<@{uid}>',embed=embed, view=Paid(self.guild_id))
        await interaction.response.send_message("📦 Account marked as sold!", ephemeral=True)

    @button(
        label='اتبند',
        custom_id='banned',
        style=ButtonStyle.red,
        emoji='⛔'
    )
    
    async def banned(self,button:Button,interaction:Interaction):
        msg = interaction.message
        channel = interaction.channel
        category_name = "Banned ⛔"
        emoji = "⛔"
        color = 0xE80000
        title = "Banned ⛔"
        desc = 'الاكونت اتبند ! ربنا يعوض عليك يا برو شوفلك واحد غيره من الجدع ده <@1323294683203375234>'
        uid = get_user_id(msg)
        embed = await move_channel(channel,category_name,emoji,color,title,desc)
        embed.add_field(name='روح هاتلك فريش جديد من هنا',value='<#1407766412830838795>')
        await msg.edit(embed=embed,view=None)
        await interaction.response.send_message("gg go next 😥",ephemeral=True)
        stats_manager.log(str(uid),'banned')

class Paid(View):
    def __init__(self,guild_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    @button(
        label='استلمت الكاش',
        custom_id='paid',
        style=ButtonStyle.green,
        emoji='💰'
    )

    async def paid(self,button: Button,interaction:Interaction):
        msg = interaction.message
        uid = get_user_id(msg)
        await interaction.response.send_modal(Money(self.guild_id,msg,uid))

    @button(
        label='اتبند',
        custom_id='banned',
        style=ButtonStyle.red,
        emoji='⛔'
    )
    
    async def banned(self,button:Button,interaction:Interaction):
        msg = interaction.message
        channel = interaction.channel
        category_name = "Banned ⛔"
        emoji = "⛔"
        color = 0xE80000
        title = "Banned ⛔"
        desc = 'الاكونت اتبند ! ربنا يعوض عليك يا برو شوفلك واحد غيره من الجدع ده <@1323294683203375234>'
        uid = get_user_id(msg)
        embed = await move_channel(channel,category_name,emoji,color,title,desc)
        embed.add_field(name='روح هاتلك فريش جديد من هنا',value='<#1407766412830838795>')
        await msg.edit(embed=embed,view=None)
        await interaction.response.send_message("gg go next 😥",ephemeral=True)
        stats_manager.log(str(uid),'banned')

class Money(Modal):
    def __init__(self,guild_id,msg,uid):
        super().__init__(title='Price 🏷️')
        self.add_item(TextInput(label='Price',placeholder='حط تمن الاكونت هنا'))
        self.guild_id = guild_id
        self.msg = msg
        self.uid = uid

    async def callback(self, interaction: Interaction):
        try:
            price = int(self.children[0].value)
        except ValueError:
            return await interaction.response.send_message('حط سعر الاكونت كا رقم بس')
        channel = interaction.channel   
        category_name = "Paid 💰"
        emoji = "💰"
        color = 0x10b8c4
        title = "الكاش وصل يا برو 🤑"
        desc = f'**Price**\n```{price} L.E```'
        embed = await move_channel(channel,category_name,emoji,color,title,desc)

        await self.msg.edit(content=f'<@{self.uid}>',embed=embed,view=None)
        await interaction.response.send_message('مليونير مليونير 💸',ephemeral=True)
        stats_manager.log(str(self.uid),'sold',price)

def setup(client):
    pass