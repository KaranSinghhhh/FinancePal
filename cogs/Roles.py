import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from dotenv import load_dotenv
import os

load_dotenv()


class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
        
    @nextcord.slash_command(name="add-roles", description="Basic Add Roles Command", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, interaction:Interaction, user : nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await interaction.response.send_message(f"{user.mention} already has the role: {role}")
        else: 
            await user.add_roles(role)
            await interaction.response.send_message(f"Added {role} to {user.mention}")
    
    @addrole.error
    async def role_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command")
        else:
            await interaction.response.send_message(f"An error occurred: {error}")
     
    @nextcord.slash_command(name="remove-roles", description="Basic Remove Roles Command", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, interaction:Interaction, user : nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"Removed {role} from {user.mention}")
        else: 
            await interaction.response.send_message(f"{user.mention} does not have this role: {role}")
    
    @removerole.error
    async def removeRole_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command")

def setup(client):
    client.add_cog(Roles(client))
