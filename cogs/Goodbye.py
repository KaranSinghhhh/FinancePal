import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from dotenv import load_dotenv
import os


load_dotenv()

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')

    
    @nextcord.slash_command(name="goodbye", description="Basic Goodbye Command", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def goodbye(self, interaction: Interaction):
        try:
            await interaction.response.send_message("Alright then mate!")
        except nextcord.Forbidden:
            print(f"I don't have permission to send messages in {interaction.channel.name}.")
        except nextcord.HTTPException:
            print("There was a problem sending the message. Please check the network connection and Discord API status.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Listener for when a member leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        try:
            channel_id = int(os.getenv('CHANNEL_ID'))  # Convert to integer
            channel = self.client.get_channel(channel_id)
            if channel:
                await channel.send(f"Goodbye, {member.display_name}!")
            else:
                print(f"Channel with ID {channel_id} not found.")
        except nextcord.Forbidden as e:
            print(f"Permission error: {e}")
        except nextcord.HTTPException as e:
            print(f"HTTP request failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def setup(client):
    client.add_cog(Goodbye(client))
