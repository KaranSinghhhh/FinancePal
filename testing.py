import requests
import json
import os

API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY') 

url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
response = requests.get(url)
data = response.json()

print(data)

if data:
    with open('sample_top_gainers_loers.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent= 4)
        print("Data written to sample_top_gainers_loers.json")
else:
    print("NO DATA TO WRITE")
    
top_gainers = data["top_gainers"]
for top_gainer in top_gainers[:5]:
    ticker = top_gainer["ticker"]
    print(f"{ticker}\n")
    
    print("-----------------------------")
    
    price = top_gainer["price"]
    print(f"{price}\n")
    
    print("-----------------------------")
    
    change_amount = top_gainer["change_amount"]
    print(f"{change_amount}\n")
    
    print("-----------------------------")
    
    change_percentage = top_gainer["change_percentage"]
    strip_percentage = change_percentage.strip("%")
    float_strip_percentage = float(strip_percentage)
    
    print(f"{float_strip_percentage:.2f}%\n")
    
    print("------------------------------")
    
    volume = top_gainer["volume"]
    print(f"{volume}")
    
    top_5_gainers = f"Ticker: {ticker}\nPrice: {price}\nChange Amount: {change_amount}\nChange_percentage: {change_percentage}\nVolume: {volume}"
    print(top_5_gainers)
    

'''
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY') 
symbol = 'AAPL'

url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()



#print(data)
if data:
       with open('sample_news_sentiment_three.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        print("Data written to sample_news_sentiment_three.json")
else:
    print("No data to write.")
'''

'''
news_feed = data['feed']

for feed in news_feed[:8]:
    feed_title = feed['title']
    #print(feed_title)
    
    feed_url = feed['url']
    #print(feed_url)
    
    feed_time_published = feed['time_published']
    date_part = feed_time_published.split('T')[0]
            
    year_part = date_part[:4]
    month_part = date_part[4:6]
    day_part = date_part[6:]
    formatted_published_dates = f"{year_part}/{month_part}/{day_part}"
    
    formatted_info = f"Title: {feed_title}\nURL: {feed_url}\nDate: {formatted_published_dates}"
    
    print(formatted_info)
    print("----------------------------------------------------")
'''


    


 
'''
def fetch_income_statement(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return {}


data = fetch_income_statement('TSLA', API_KEY)
if data:
    with open('sample_news_sentiment_two.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("Data written to sample_news_sentiment_two.json")
else:
    print("No data to write.")
'''

'''
annual_reports = data['annualReports']
for report in annual_reports: 
    fiscal_date_ending_report = report['fiscalDateEnding'] #Get all the annual fiscal dates
    print(fiscal_date_ending_report)
'''