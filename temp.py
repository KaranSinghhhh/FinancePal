import nextcord
from nextcord.ext import commands
from nextcord import member
from nextcord.ext.commands import has_permissions, MissingPermissions
import requests
from dotenv import load_dotenv
import os



client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())  #Whenever a uses includes a "!" in a chat, the bot knows that the message is for it



@client.event #When a event detects a certain action, it will execute a certain piece of code
async def on_ready():
    await client.change_presence (status=nextcord.Status.idle, activity = nextcord.Game("Subscribe"))  #idle can be changed to invisible, online, and more...
    print("The bot is now ready for use!")
    print("----------------------------- ")
    
@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the Karan Bot")
    
@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye!")
    
@client.event
async def on_member_join(member):
    load_dotenv() 
    jokeurl = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_JOKE_KEY'),
        "X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
    }

    try:
        response = requests.get(jokeurl, headers=headers)
        response.raise_for_status()
        jokes = response.json()  # Directly get JSON

        # Assuming the API returns a list of jokes, we take the first one
        if jokes and isinstance(jokes, list) and 'joke' in jokes[0]:
            first_joke = jokes[0]['joke']
        else:
            first_joke = "No joke found."

    except Exception as e:
        print(f"An error occurred: {e}")
        first_joke = "Sorry, I couldn't fetch a joke right now."

    channel_id = os.getenv('CHANNEL_ID')
    channel = client.get_channel(channel_id)
    await channel.send("Welcome! Here is a joke")
    await channel.send(first_joke)  # Send only the joke text

@client.event
async def on_member_remove(member):
    load_dotenv()
    channel_id = os.getenv('CHANNEL_ID')
    channel = client.get_channel(channel_id)
    await channel.send("Goodbye")
    

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else: 
        await ctx.send("You are not in a voice channel!")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I Left the voice channel")
    else:
        await ctx.send("I am not in the voice channel")
        
@client.event
async def on_message(message):
    if message.content == "Hi":
        await message.delete()
        await message.channel.send("Don't send that again!")
    await client.process_commands(message)
    
@client.command()
@has_permissions(kick_members = True)
async def kick(ctx, member: nextcord.Member, *, reason = None):
    print(f"Attempting to kick: {member}, Reason: {reason}") 
    await member.kick(reason = reason)
    await ctx.send(f"User  {member} has been kicked")
    
@kick.error 
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")
    else:
        # Log other types of errors
        print(f"Unhandled error: {error}")

@client.command()
@has_permissions(ban_members = True)
async def ban(ctx, member: nextcord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"User {member} has been banned")
    
@ban.error 
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people!")

@client.command()
async def embed(ctx):
    embed = nextcord.Embed(title = "Dog", url="https://google.com", description = "We love Dogs", color = 0x4dff4d )
    embed.set_author(name=ctx.author.display_name, url="https://google.com",icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url="")
    embed.add_field(name="Labradore", value="Cute Dog", inline=True)
    embed.add_field(name="Pugs", value="Cute Dog", inline=True)
    embed.set_footer(text="Thank you for reading")
    await ctx.send(embed = embed)

#Discord.py error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to run this command")
        

@client.command()
async def message(ctx, user:nextcord.Member, *, message = None):
    message = "Welcome to the server buddy!"
    embed = nextcord.Embed(title=message)
    await user.send(embed=embed)


client.run(os.getenv('DISCORD_TOKEN'))