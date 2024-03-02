import requests
import json
import os


API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY') 
symbol = 'AAPL'
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
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
    
news_feed = data['feed']
for feed in news_feed:
    feed_title = feed['title']
    
    
    feed_time_published = feed['time_published']
    date_part = feed_time_published.split('T')[0]
    print(date_part)
            
    year_part = date_part[:4]
    month_part = date_part[4:6]
    day_part = date_part[6:]
    
    formatted_published_data = f"{year_part}/{month_part}/{day_part}"
    
   
        
    


 
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