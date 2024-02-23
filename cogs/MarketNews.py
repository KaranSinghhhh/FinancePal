
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
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()     



def setup(client):
    client.add_cog(MarketNews(client))
