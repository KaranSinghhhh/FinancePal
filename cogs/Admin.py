import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import os

load_dotenv()

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
   
    testServerId = os.getenv('TEST_SERVER_ID')
                   
        
    @nextcord.slash_command(name="kick", description="Basic kick Command", guild_ids=[testServerId])
    @has_permissions(kick_members=True)
    async def kick(self, interaction:Interaction, member: nextcord.Member, *, reason=None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"User {member} has been kicked")
        
    @kick.error 
    async def kick_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to kick people!")
        else:
            await interaction.response.send_message("An error occurred while processing the command.")
            print(f"Unhandled error: {error}")
            
    @nextcord.slash_command(name="ban", description="Basic ban Command", guild_ids=[testServerId])
    @has_permissions(ban_members=True)
    async def ban(self, interaction: Interaction, member: nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"User {member} has been banned")
    
    @ban.error 
    async def ban_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to ban people!")
        else:
            await interaction.response.send_message("An error occurred while processing the command.")
            print(f"Unhandled error: {error}")
            
    @nextcord.slash_command(name="unban", description="Basic unban Command", guild_ids=[testServerId])
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction:Interaction, *, member):
        member_name, member_discriminator = member.split('#')

        async for ban_entry in interaction.guild.bans():
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'Unbanned {user.mention}')
                return

        # If the user was not found in the ban list
        await interaction.response.send_message("User not found in ban list")
    
    @unban.error
    async def unban_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to unban people")
        else:
            await interaction.response.send_message("An error occurred while processing the command.")
            print(f"Unhandled error: {error}")
    
    '''  
    @commands.command()
    @commands.has_guild_permissions(manage_messages = True)
    async def delete(self, ctx, *, delay = None, Reason = None, member: discord.Member):
        await member.delete(reason = Reason)
        await ctx.send("This message has been deleted by the bot")
    '''   
            

def setup(client):
    client.add_cog(Admin(client))
