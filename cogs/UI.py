import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import os


load_dotenv()



class Subscriptions(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None) #timeout can be changed to a specific time
        self.value = None

    @nextcord.ui.button(label = "Subscribe", style = nextcord.ButtonStyle.blurple)
    async def subscribe(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Thanks for subscribing to me!", ephemeral=False) #ephemeral = False means everyone can see this message 
        self.value = True
        self.stop()
        
    @nextcord.ui.button(label = "You should Subscribe", style = nextcord.ButtonStyle.red)
    async def shouldsubscribe(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("There's onle one option!", ephemeral=False) #ephemeral = False means everyone can see this message 
        self.value = True
        self.stop()
        
class Dropdown(nextcord.ui.Select):
    def __init__(self):
        selectoptions = [
            nextcord.SelectOption(label="Subscribe", description="Subscribe to my socail media"),
            nextcord.SelectOption(label="DoSubscribe", description="Do Subscribe to my socail media"),
            nextcord.SelectOption(label="MustSubscribe", description="You must Subscribe to my socail media")
        ]
        
        super().__init__(placeholder="Subscribe Options", min_values = 1, max_values=1, options = selectoptions)
            
    async def callback(self, interaction:Interaction):
        if self.values[0] == "Subscribe":
            return await interaction.response.send_message("Thank you for subscribing!")
        elif self.values[0] == "DoSubscribe":
            return await interaction.response.send_message("Thank you for subscribing!")
        elif self.values[0] == "MustSubscribe":
            return await interaction.response.send_message("Thank you for subscribing!")

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class UI(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    testServerId = os.getenv('TEST_SERVER_ID')
    
    @nextcord.slash_command(name= "button", description="Subscribe button", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def sub(self, interaction: Interaction):
        view = Subscriptions()
        await interaction.response.send_message("You have two options:", view = view)
        await view.wait()
        
        if view.value is None:
            return

        elif view.value:
            print("yay subscribed")
        else:
            print("Yayy you still subscribed")

    @nextcord.slash_command(name = "dropdown", description="Dropdown Test", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def drop(self, interaction: Interaction):
        view = DropdownView()
        await interaction.response.send_message("Do you want to subscribe:", view=view)

def setup(client):
    client.add_cog(UI(client))
