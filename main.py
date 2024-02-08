import nextcord
from nextcord.ext import commands
import cog_registration  # Import cog registration file
import traceback
from dotenv import load_dotenv
import os

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@client.event
async def on_ready():
    print("The bot is now ready for use!")
    print("----------------------------- ")
    await load_cogs()

async def load_cogs():
    for cog in cog_registration.COGS:
        try:
            client.load_extension(cog)
            print(f"Successfully loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}. Error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    
    client.run(discord_token)
