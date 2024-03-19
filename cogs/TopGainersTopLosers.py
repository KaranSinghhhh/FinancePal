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
    
    def get_Top_Gainers_Top_Losers(self, symbol):
        try:
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}'
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
                    
            
def setup(client):
    client.add_cog(TopGainersTopLosers(client))

        

