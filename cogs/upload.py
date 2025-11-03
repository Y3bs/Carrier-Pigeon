from nextcord.ext import commands
from nextcord import Interaction,SlashOption,Attachment,Embed,slash_command
import utils.database as db


class Upload(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='upload',description="Upload a .txt account file and store its content")
    async def upload(self,interaction: Interaction,
        game: str = SlashOption(
            name='game',
            description='Game type (e.g., warzone)',
            choices=['Warzone',"Marvel Rivals"],
            required=True
        ),
        file:Attachment = SlashOption(
        name='acc_file',
        description='Upload a .txt file',
        required=True
    )):
        await interaction.response.defer(ephemeral=True)
        if not interaction.guild or not interaction.user.guild_permissions.administrator:
            error = Embed(
                title = 'Guild/Permission Error ⛔',
                description='This command can only run in:\n> Server with Admin Permission',
                color = 0xE80000
            )
            return await interaction.followup.send(embed=error , ephemeral=True)

        if not file.filename.lower().endswith('.txt'):
            return await interaction.followup.send('ارفع فايل .txt انت عايز تهكرني ؟ 😡')
        file_bytes = await file.read()
        try:
            file_content = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return await interaction.followup.send('تعذر قراءة الملف كنص UTF-8.')

        ok = db.save_account(interaction.user.id, game, file_content, interaction.guild.id)
        if ok:
            embed = Embed(title="✅ Saved", description=f"تم حفظ الحساب لِلعبة: `{game}`")
            return await interaction.followup.send(embed=embed)
        else:
            embed = Embed(title="❌ Error", description="حدث خطأ أثناء الحفظ")
            return await interaction.followup.send(embed=embed)


def setup(client):
    client.add_cog(Upload(client))