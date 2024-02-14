import requests
import json
import os


API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY') or 'your_api_key_here'


def fetch_income_statement(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return {}


data = fetch_income_statement('AAPL', API_KEY)
if data:
    with open('cash_flow.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("Data written to income_statement.json")
else:
    print("No data to write.")


annual_reports = data['annualReports']
for report in annual_reports: 
    fiscal_date_ending_report = report['fiscalDateEnding'] #Get all the annual fiscal dates
    print(fiscal_date_ending_report)