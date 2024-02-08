
import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class MarketNews(commands.Cog):
    def __init__(self, client):
        self.client = client

   
   

    def get_market_news(self, symbol):
        try:
            api_key = "LFCWIHIIY5SRPB7N"  
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

           
            news_items = data.get('news_sentiment', [])

            ticker_values_list = []
            for item in news_items:
                for ticker_info in item.get('ticker_sentiment', []):
                    if ticker_info.get('ticker') == symbol:
                        ticker_values = {
                            "Ticker": ticker_info['ticker'],
                            "Relevance Score": ticker_info['relevance_score'],
                            "Ticker Sentiment Score": ticker_info['ticker_sentiment_score'],
                            "Ticker Sentiment Label": ticker_info['ticker_sentiment_label']
                        }
                        ticker_values_list.append(ticker_values)
            return ticker_values_list

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @nextcord.slash_command(name="market-news", description="Get market news", guild_ids='')
    async def market_news_command(self, interaction: Interaction, symbol: str):
        market_news = self.get_market_news(symbol)
        if market_news:
            response = "\n".join([f"Ticker: {ticker['Ticker']}, Relevance Score: {ticker['Relevance Score']}, Sentiment Score: {ticker['Ticker Sentiment Score']}, Label: {ticker['Ticker Sentiment Label']}" for ticker in market_news])
            await interaction.response.send_message(response)
        else:
            await interaction.response.send_message(f"No market news found for {symbol} or there was an error.")

def setup(client):
    client.add_cog(MarketNews(client))
