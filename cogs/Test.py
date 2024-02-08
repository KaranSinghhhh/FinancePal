import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Test cog has been initialized")  # Log initialization

    testServerId = 728273598669651978
    
    @nextcord.slash_command(name="test", description="This is a test command", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def test(self, interaction: nextcord.Interaction):
        print("Test command has been triggered")  # Log when the command is triggered
        embed = nextcord.Embed(title="Test Embed")
        embed.set_author(name="FinancePal", icon_url="https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b")
        await interaction.response.send_message(embed=embed)

        await interaction.response.send_message("This is a test!")
        print("Test command executed and response sent")  # Log after sending the response



def setup(client):
    client.add_cog(Test(client))
    print("Test cog has been loaded")  
