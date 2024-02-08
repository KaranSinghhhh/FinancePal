import nextcord
from nextcord.ext import commands

# Replace 'your_token_here' with your bot's token
BOT_TOKEN = 'MTE5MDAzMTgxMzQxOTIwODg0NQ.Gi4ysD.tjMYdkPbKCwTmbYix6MVTE6-M56Qe6eiiM6T1c'

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(guild_ids=[728273598669651978])  # Replace with your guild ID
async def test_command(interaction: nextcord.Interaction):
    await interaction.response.send_message("Test command works!")

bot.run(BOT_TOKEN)
