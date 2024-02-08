import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os


load_dotenv()


import matplotlib
matplotlib.use('Agg')

class stocks(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')

    

    '''
    def fetch_logo_image_url(self, symbol):
        api_url = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
        try:
            response = requests.get(api_url, headers={'X-Api-Key': ''})

            if response.status_code == 200:
                data = response.json()
                if data and 'image' in data[0]:
                    return data[0]['image']
                else:
                    return "No image found."
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.RequestException as e:
            return f"Error: {e}"
    '''
       
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




        
    
    def get_stock_data(self, symbol):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={os.environ['ALPHA_VANTAGE_API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            
            # Extracting the latest data
            last_refreshed = data["Meta Data"]["3. Last Refreshed"]
            latest_data = data["Time Series (Daily)"][last_refreshed]
            stock_values = {
                "Open": latest_data["1. open"],
                "High": latest_data["2. high"],
                "Low": latest_data["3. low"],
                "Close": latest_data["4. close"],
                "Volume": latest_data["5. volume"]
            }
            
        
            day_before_data_keys = list(data["Time Series (Daily)"])  # Get the list of keys (dates)
            day_before_date = day_before_data_keys[1]  # Access the second key (date)

            # Now use this date to get the stock values
            day_before_data_values = data["Time Series (Daily)"][day_before_date]

            # Extract the close and volume values
            day_before_data_stock_values = {
                "Close": day_before_data_values["4. close"],
                "Volume": day_before_data_values["5. volume"]
            }
            
            return stock_values, day_before_data_stock_values
           
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
       

    @nextcord.slash_command(name="stock-info", description="Gets stock info", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def stock(self, interaction: Interaction, symbol: str):
        latest_stock_info, day_before_stock_info = self.get_stock_data(symbol)
        
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
       
        
        try:
            if latest_stock_info and day_before_stock_info:
                
                
                latest_close = float(latest_stock_info["Close"])
                previous_close = float(day_before_stock_info["Close"])      
                
                close_difference = round(latest_close - previous_close, 2)
                close_percent_difference = round(((latest_close - previous_close) / previous_close) * 100, 2)
                
                close_difference_str = f"${close_difference}"
                close_percent_difference_str = f"{close_percent_difference}%"
                
                latest_volume = int(latest_stock_info["Volume"])
                previous_volume = int(day_before_stock_info["Volume"])
                
                volume_difference = latest_volume - previous_volume
                volume_percent_difference = round(((latest_volume - previous_volume) / previous_volume) * 100 ,2)
                
                volume_difference_str = f"{volume_difference}"
                volume_percent_difference_str = f"{volume_percent_difference}%"
                
                bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
                
                
                
                embed = nextcord.Embed(title=f"{symbol} Stock", url = bloomberg_url ,description="Market Close Date Information", color=0x4dff4d)
               
                '''
                if logo_url.startswith(("http://", "https://")):
                    embed.set_thumbnail(url=logo_url)
                else:
                    print(f"Logo URL not valid for symbol {symbol}: {logo_url}")
                '''
                
                if logo_url and logo_url.startswith(("http://", "https://")):
                    embed.set_thumbnail(url=logo_url)
                    
                current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
                embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
                
                finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
                embed.set_author(name="FinancePal", icon_url=finance_pal_url)
            
                embed.add_field(name="Close Price", value=f"${latest_stock_info['Close']}", inline=True)
                embed.add_field(name="Close Price Change", value=close_difference_str, inline=True)
                embed.add_field(name="Close Percent Change ", value=close_percent_difference_str, inline=True)
                
                embed.add_field(name="Open Price", value= "$" + str(round(float(latest_stock_info['Open']), 2)), inline=True)
                embed.add_field(name="High Price", value= "$" + str(round(float(latest_stock_info['High']), 2)), inline=True)
                embed.add_field(name="Low Price", value= "$" + str(round(float(latest_stock_info['Low']), 2)), inline=True)
               
            
               
                embed.add_field(name= "Volume", value=latest_stock_info['Volume'], inline= True)
                if "-" not in volume_difference_str:
                    embed.add_field(name= "Volume Change", value="+" + str(volume_difference_str), inline=True)
                else:
                    embed.add_field(name= "Volume Change", value=volume_difference_str, inline=True)
                embed.add_field(name= "Volume Percent Change", value= volume_percent_difference_str, inline=True)
                
                
               

                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve stock data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
            
    def get_weekly_stock_data(self, symbol):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={os.environ['ALPHA_VANTAGE_API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Extracting the latest weekly data
            last_refreshed = list(data["Weekly Time Series"].keys())[0]
            latest_weekly_data = data["Weekly Time Series"][last_refreshed]
            weekly_stock_values = {
                "Open": latest_weekly_data["1. open"],
                "High": latest_weekly_data["2. high"],
                "Low": latest_weekly_data["3. low"],
                "Close": latest_weekly_data["4. close"],
                "Volume": latest_weekly_data["5. volume"]
            }
            return weekly_stock_values
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    @nextcord.slash_command(name="stock-info-weekly", description="Gets weekly stock info", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def stock_weekly(self, interaction: Interaction, symbol: str):
        weekly_stock_info = self.get_weekly_stock_data(symbol)
        try:
            if weekly_stock_info:
                embed = nextcord.Embed(title=f"Weekly Stock Data for {symbol}", description="Weekly info for ticker:", color=0x4dff4d)
                embed.add_field(name="Open", value=weekly_stock_info['Open'], inline=True)
                embed.add_field(name="High", value=weekly_stock_info['High'], inline=True)
                embed.add_field(name="Low", value=weekly_stock_info['Low'], inline=True)
                embed.add_field(name="Close", value=weekly_stock_info['Close'], inline=True)
                embed.add_field(name="Volume", value=weekly_stock_info['Volume'], inline=True)
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Weekly stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve weekly stock data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

    @nextcord.slash_command(name="stock-chart-weekly", description="Gets daily stock chart", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def stock_chart_weekly(self, interaction: Interaction, symbol: str):
        # Fetch the full time series data
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={os.environ['ALPHA_VANTAGE_API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            daily_stock_data = response.json()

            if 'Time Series (Daily)' not in daily_stock_data:
                await interaction.response.send_message("Failed to retrieve daily stock data.")
                return

            # Process and format the data
            df = pd.DataFrame.from_dict(daily_stock_data['Time Series (Daily)'], orient='index', dtype=float)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df.index = pd.to_datetime(df.index)
            
            # Ensure the DataFrame is sorted by date
            df.sort_index(inplace=True)

            # Filter the DataFrame to the last 5 rows for the most recent week
            df = df.last('5D')

            # Create a candlestick chart with mplfinance
            mpf_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})
            fig, ax = mpf.plot(df, type='candle', style=mpf_style, volume=False, returnfig=True,
                            datetime_format='%Y-%m-%d', show_nontrading=True, figsize=(10, 5), tight_layout=True)

           
                        
            
            
            # Save the chart to a BytesIO object
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=300)  # You can adjust the dpi for image quality
            buffer.seek(0)

            # Send the image to the user's DMs
            file = nextcord.File(buffer, filename=f"{symbol}_daily_chart.png")
            await interaction.user.send(file=file)
            await interaction.response.send_message(f"Daily stock chart sent to your DMs.", ephemeral=False)
        except requests.RequestException as e:
            await interaction.response.send_message(f"An error occurred while fetching data: {e}")

    @nextcord.slash_command(name="stock-chart-monthly", description="Gets daily stock chart", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def stock_chart_monthly(self, interaction: Interaction, symbol: str):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={os.environ['ALPHA_VANTAGE_API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            daily_stock_data = response.json()

            if 'Time Series (Daily)' not in daily_stock_data:
                await interaction.response.send_message("Failed to retrieve daily stock data.")
                return
            
            df = pd.DataFrame.from_dict(daily_stock_data['Time Series (Daily)'], orient='index', dtype=float)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df.index = pd.to_datetime(df.index)
            
            # Ensure the DataFrame is sorted by date
            df.sort_index(inplace=True)

            # Select the last 21 rows for the past month's worth of trading data
            df = df.iloc[-21:]
            
            mpf_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})
            fig, ax = mpf.plot(df, type='candle', style=mpf_style, volume=False, returnfig=True,
                            datetime_format='%Y-%m-%d', show_nontrading=True, figsize=(10, 5), tight_layout=True)

           # Save the chart to a BytesIO object
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=300)  # You can adjust the dpi for image quality
            buffer.seek(0)

            # Send the image to the user's DMs
            file = nextcord.File(buffer, filename=f"{symbol}_daily_chart.png")
            await interaction.user.send(file=file)
            await interaction.response.send_message(f"Daily stock chart sent to your DMs.", ephemeral=False)
        except requests.RequestException as e:
            await interaction.response.send_message(f"An error occurred while fetching data: {e}")
            


def setup(client):
    client.add_cog(stocks(client))



