from nextcord.ext import commands
from nextcord import Interaction,SlashOption,Attachment,Embed,slash_command

from utils.fresh_manager import fresh_manager


class Upload(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @slash_command(name='upload',description="Uploads the .txt file of the account to the bot's data base")
    async def upload(self,interaction: Interaction,file:Attachment = SlashOption(
        name='acc_file',
        description='Upload a .txt file',
        required=True
    )):
        await interaction.response.defer(ephemeral=True)

        if not file.filename.lower().endswith('.txt'):
            return await interaction.followup.send('ارفع فايل .txt انت عايز تهكرني ؟ 😡')
        file_bytes = await file.read()
        file_content = file_bytes.decode('utf-8')
        file_name = fresh_manager.upload_file(file_content,'warzone')
        if file_name:
            embed = Embed(
            title="✅ File uploaded!",
            description=f"```Game: warzone\nName: {file_name}```"
            )
            return await interaction.followup.send(embed=embed)
        else:
            error = Embed(
                title='Error saving file',
                description='Something wrong happned while saving the file',
                color=0xE80000
            )
            return await interaction.followup.send(embed=error)


def setup(client):
    client.add_cog(Upload(client))