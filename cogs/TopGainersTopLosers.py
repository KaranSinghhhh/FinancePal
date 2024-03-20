import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv
from datetime import datetime

class TopGainersTopLosers(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
    
    def get_Top_Gainers_Top_Losers(self):
        try:
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
            url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}'
            response = requests.get(url)
            data = response.json()     
            
            if "top_gainers" in data:
                top_gainers = data["top_gainers"]
                top_5_gainers_list = []
            
                for top_gainer in top_gainers[:5]:
                    
                    ticker = top_gainer["ticker"]
                    #print(f"{ticker}\n")
                    
                    price = top_gainer["price"]
                    #print(f"{price}\n")
                    
                    change_amount = top_gainer["change_amount"]
                    #print(f"{change_amount}\n")
                    
                    change_percentage = top_gainer["change_percentage"]
                    strip_percentage = change_percentage.strip("%")
                    float_strip_percentage = float(strip_percentage)
                    round_float_strip_percentage= f"{float_strip_percentage:.2f}%\n"
                    volume = top_gainer["volume"]
                    
                    top_5_gainers = f"Ticker: {ticker}\nPrice: {price}\nChange Amount: {change_amount}\nChange_percentage: {round_float_strip_percentage}\nVolume: {volume}"
                    #print(top_5_gainers)
                    top_5_gainers_list.append(top_5_gainers)

                return top_5_gainers_list
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    @nextcord.slash_command(name="top-5-gainers-losers", description="Gets The Top 5 Gainers and Losers of the day", guild_ids=[int(testServerId)])
    async def stock(self, interaction: Interaction):
        latest_top_5_gainers_losers = self.get_Top_Gainers_Top_Losers()

        
        try:
            if latest_top_5_gainers_losers:
                embed = nextcord.Embed(title=f"Top 5 gainers and losers", description="Here's the latest market news:", color=0x4dff4d)
                
                current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
                embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
                
                finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
                embed.set_author(name="FinancePal", icon_url=finance_pal_url)
                
                
                for item in latest_top_5_gainers_losers:
                    # Each item is added as a value of a single field
                    embed.add_field(name="\u200B", value=item, inline=False)  # Use zero-width space for an invisible field name
                
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message(f"Failed to retrieve top 5 gainers or losers", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        
def setup(client):
    client.add_cog(TopGainersTopLosers(client))

        

