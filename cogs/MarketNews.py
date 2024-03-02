
import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime
import os
from dotenv import load_dotenv

#Load environment variable
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
            
            
            news_feed = data['feed']
            
            for feed in news_feed:
                news_items = []
                
                feed_title = feed['title']
            
                feed_time_published = feed['time_published']
                date_part = feed_time_published.split('T')[0]
                
                year_part = date_part[:4]
                month_part = date_part[4:6]
                day_part = date_part[6:]
                
                formatted_published_data = f"{year_part}/{month_part}/{day_part}"
                
                news_items.append((feed_title, formatted_published_data ))
                
                return news_items
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    @nextcord.slash_command(name="market-news", description = "Gets Market News ",  guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def stock(self, interaction: Interaction, symbol: str):
        latest_market_news = self.get_news_sentiment(symbol)
        
        try:
            if latest_market_news:
                embed = nextcord.Embed(title=f"Market News for {symbol}", description="Market News for ticker:", color=0x4dff4d)
                
                for title, publish_date in latest_market_news:
                    embed.add_field(name="Title", value=title , inline=True)
                    embed.add_field(name="Publish Date", value=publish_date ,  inline=True)
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message(f"Failed to retrieve market news for {symbol}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

def setup(client):
    client.add_cog(MarketNews(client))
