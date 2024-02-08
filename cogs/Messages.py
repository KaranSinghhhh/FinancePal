import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from collections import defaultdict

forbidden_messages = []


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.forbidden_message_counter = defaultdict(int)
        self.ban_on_forbidden_message_counter = 0
     
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.name + " added:" + reaction.emoji)
        
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.name + " removed:" + reaction.emoji)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        #Prevent the bot from reacting to it self
        if message.author == self.client.user:
            return
    
        if("happy") in message.content:
            emoji = "😂"
            await message.add_reaction(emoji)
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        user_id = message.author.id
        
        for badmessage in forbidden_messages:
            if badmessage in message.content:
                try:
                    
                    self.forbidden_message_counter[user_id] += 1
                    print(f"User {user_id} forbidden message count: {self.forbidden_message_counter[user_id]}")
                    await message.delete()
                    await message.channel.send("This is a forbidden message!")
                    
                    forbidden_message = f"You said a forbidden word in chat, and your message in chat was deleted. This is how many warnings you have: {self.forbidden_message_counter[user_id]} warnings. Total of 3 warnings will result in an automatic kick from Server!"
                    embed = nextcord.Embed(title=forbidden_message)
                    await message.author.send(embed=embed)
                    
                    if self.forbidden_message_counter[user_id] == 3:
                        await message.author.kick(reason = "Repeated use of a forbidden message")
                        self.forbidden_message_counter[user_id] = 0
                        
                    
                    
                except nextcord.Forbidden as e:
                    print(f"Permission error: {e}")
                except nextcord.HTTPException as e:
                    print(f"HTTP request failed: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
      
      
            
        

    
    
def setup(client):
    client.add_cog(Messages(client))
