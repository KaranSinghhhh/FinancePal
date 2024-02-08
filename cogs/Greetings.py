import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import member
from nextcord.ext.commands import has_permissions, MissingPermissions
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Greetings cog initialized")  
                   

    @nextcord.slash_command(name="hello", description="Basic Greeting Command", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def hello(self, interaction: Interaction):
        print("Hello command triggered") 
        try:
            await interaction.response.send_message("Hello, I am the Karan Bot")
            print("Message sent successfully")  
        except Exception as e:
            print(f"Error in sending message: {e}")  

              
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # fetch and send a joke to a specific channel
        load_dotenv() 
        jokeurl = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPID_API_JOKE_KEY'),
            "X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(jokeurl, headers=headers) as response:
                    if response.status == 200:
                        jokes = await response.json()
                        first_joke = jokes[0]['joke'] if jokes else "No joke found."
                    else:
                        first_joke = "Sorry, I couldn't fetch a joke right now."
            except Exception as e:
                print(f"An error occurred: {e}")
                first_joke = "Sorry, I couldn't fetch a joke right now."

        channel_id = int(os.getenv('CHANNEL_ID'))  # Convert to integer
        channel = self.client.get_channel(channel_id)
        if channel:
            await channel.send("Welcome! Here is a joke")
            await channel.send(first_joke)

        # Send a DM to the new member
        welcome_message = "Welcome to the server buddy!"
        try:
            embed = nextcord.Embed(title=welcome_message)
            await member.send(embed=embed)
        except Exception as e:
            print(f"An error occurred while sending DM: {e}")

def setup(client):
   client.add_cog(Greetings(client))
