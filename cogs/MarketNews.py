import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variable
load_dotenv()

class MarketNews(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
    
    def fetch_logo_image_url(self, symbol):
        api_key = os.environ['API_NINJAS_KEY'] 
        api_url_name = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
        api_url_ticker = f'https://api.api-ninjas.com/v1/logo?name={symbol}&ticker=true'
        
        try:
            response = requests.get(api_url_name, headers={'X-Api-Key': api_key})
            if response.status_code == 200 and response.json():
                data = response.json()
                if 'image' in data[0]:
                    return data[0]['image']

            response_ticker = requests.get(api_url_ticker, headers={'X-Api-Key': api_key})
            if response_ticker.status_code == 200 and response_ticker.json():
                data_ticker = response_ticker.json()
                if 'image' in data_ticker[0]:
                    return data_ticker[0]['image']

            print(f"No image found for symbol {symbol}.")
            return None
        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return None



    def get_company_name_from_ticker(self, symbol):
        api_key = os.environ['ALPHA_VANTAGE_API_KEY']
        endpoint = f'https://www.alphavantage.co/query'
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': symbol,
            'apikey': api_key,
        }

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200 and response.json():
                data = response.json()
                if 'bestMatches' in data and data['bestMatches']:
                    full_name = data['bestMatches'][0]['2. name']
                    company_name = full_name.split(' ')[0]  # Split by space and take the first part
                    return company_name
            return None
        except requests.RequestException as e:
            print(f"Error fetching company name: {e}")
            return None


    
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
        
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
       
        
        bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
        
        try:
            if latest_market_news:
                embed = nextcord.Embed(title=f"Market News for {symbol}", url=bloomberg_url, description="Here's the latest market news:", color=0x4dff4d)
                if logo_url and logo_url.startswith(("http://", "https://")):
                    embed.set_thumbnail(url=logo_url)
                
                current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
                embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
                
                finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
                embed.set_author(name="FinancePal", icon_url=finance_pal_url)
                
                
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

