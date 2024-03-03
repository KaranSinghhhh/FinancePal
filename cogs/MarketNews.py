import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

class MarketNews(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
    
    def get_news_sentiment(self, symbol):
        try:
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}'
            response = requests.get(url)
            data = response.json()     
            
            if 'feed' in data:  # Check if 'feed' is in the response
                news_feed = data['feed']
                news_items = []  # Initialize the list outside the loop

                for feed in news_feed[:8]:  # Process first 8 news items
                    feed_title = feed['title']
                    feed_url = feed['url']
                    feed_time_published = feed['time_published']
                    date_part = feed_time_published.split('T')[0]

                    year_part = date_part[:4]
                    month_part = date_part[4:6]
                    day_part = date_part[6:]

                    formatted_published_date = f"{year_part}-{month_part}-{day_part}"
                    formatted_information = f"**Title:** {feed_title}\n**URL:** <{feed_url}>\n**Date:** {formatted_published_date}"

                    news_items.append(formatted_information)  # Append to list inside the loop

                return news_items  # Return the list after the loop completes
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    @nextcord.slash_command(name="market-news", description="Gets Market News", guild_ids=[int(testServerId)])
    async def stock(self, interaction: Interaction, symbol: str):
        latest_market_news = self.get_news_sentiment(symbol)
        
        try:
            if latest_market_news:
                embed = nextcord.Embed(title=f"Market News for {symbol}", description="Here's the latest market news:", color=0x4dff4d)
                
                for item in latest_market_news:
                    # Each item is added as a value of a single field
                    embed.add_field(name="\u200B", value=item, inline=False)  # Use zero-width space for an invisible field name
                
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message(f"Failed to retrieve market news for {symbol}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

def setup(client):
    client.add_cog(MarketNews(client))

