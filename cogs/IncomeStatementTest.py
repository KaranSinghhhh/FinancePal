import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class IncomeStatement(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = int(os.getenv('TEST_SERVER_ID'))
    
    def fetch_logo_image_url(self, symbol):
        api_key = os.getenv('API_NINJAS_KEY')  
        api_url_name = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
        api_url_ticker = f'https://api.api-ninjas.com/v1/logo?name={symbol}&ticker=true'
        
        try:
            response = requests.get(api_url_name, headers={'X-Api-Key': api_key})
            print(f"API Response (name): {response.json()}")  # Debugging line
            if response.status_code == 200 and response.json():
                data = response.json()
                if 'image' in data[0]:
                    return data[0]['image']

            response_ticker = requests.get(api_url_ticker, headers={'X-Api-Key': api_key})
            print(f"API Response (ticker): {response_ticker.json()}")  # Debugging line
            if response_ticker.status_code == 200 and response_ticker.json():
                data_ticker = response_ticker.json()
                if data_ticker and 'image' in data_ticker[0] and symbol.lower() == data_ticker[0]['ticker'].lower():
                    return data_ticker[0]['image']

            print(f"No image found for symbol {symbol}.")
            return None
        except requests.RequestException as e:
            print(f"Request exception: {e}")
            return None



    def get_company_name_from_ticker(self, symbol):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY') 
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
        
    

    
    def fetch_income_statement_data(self, symbol, fiscal_date_ending_report):
        try:
            url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            annual_reports = data['annualReports']
            
            #Getting the fiscal date as an option for the user to select
            for report in annual_reports:
                fiscal_date_ending_report = [report['fiscalDateEnding']]
                print(fiscal_date_ending_report)
                
            income_statement_values = {
                "ReportedCurrency": report["reportedCurrency"],
                "GrossProfit": report["grossProfit"],
                "TotalRevenue": report["totalRevenue"],
                "CostOfRevenue": report["costOfRevenue"],
                "CostOfGoodsAndServicesSold": report["costOfGoodsAndServicesSold"],
                "OperatingIncome": report["operatingIncome"],
                "SellingGeneralAndAdministrative": report["sellinGeneralAndAdministrative"],
                "ResearchAndDevelopment": report["researchAndDevelopment"],
                "OperatingExpenses": report["operatingExpenses"],
                "InvestmentIncomeNet": report["investmentIncomeNet"],
                "NetInterestIncome": report["netInterestIncome"],
                "InterestIncome": report["interestIncome"],
                "InterestExpense": report["interestExpense"],
                "NonInterestIncome": report["nonInterestIncome"],
                "OtherNonOperatingIncome": report["otherNonOperatingIncome"],
                "Depreciation": report["depreciation"],
                "DepreciationAndAmortization": report["depreciationAndAmortization"],
                "IncomeBeforeTax": report["incomeBeforeTax"],
                "IncomeTaxExpense": report["incomeTaxExpense"],
                "InterestandDebtExpense": report["interestAndDebtExpense"],
                "NetIncomeFromContinuingOperations": report["netIncomeFromContinuingOperations"],
                "ComprehensiveIncomeNetOfTax": report["comprehensiveIncomeNetOfTax"],
                "Ebit": report["ebit"],
                "Ebitda": report["ebitda"],
                "NetIncome": report["netIncome"]
            }
            return income_statement_values
                
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
      
    @nextcord.slash_command(name="income-info", description="Gets Income Info", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def company_info(self, interaction: Interaction, symbol: str):
        the_income_info = self.get_company_info(symbol)
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
       
        
        
        try: 
            if the_income_info:
                bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
                
                
                embed = nextcord.Embed(title=f"{symbol} Stock", url=bloomberg_url, description="Info for Ticker:", color=0x4dff4d)
                
                    
                if logo_url and logo_url.startswith(("http://", "https://")):
                    embed.set_thumbnail(url=logo_url)
                    
                current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
                embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
                
                finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
                embed.set_author(name="FinancePal", icon_url=finance_pal_url)
                
                embed.add_field(name="Reported Currency", value=the_income_info['ReportedCurrency'], inline=True)
                embed.add_field(name="Gross Profit", value=f"${the_income_info['GrossProfit']}", inline=True)
                embed.add_field(name="Total Revenue", value=f"{the_income_info['TotalRevenue']}", inline=False)
                embed.add_field(name="Cost Of Revenue", value=f"{the_income_info['CostOfRevenue']}", inline=False)
                embed.add_field(name="Cost of Goods and Services Sold", value=the_income_info['CostOfGoodsAndServicesSold'], inline=False)
                embed.add_field(name="Operating Income", value=the_income_info['OperatingIncome'], inline=True)
                embed.add_field(name="Selling General and Administrative", value=the_income_info['SellingGeneralAndAdministrative'], inline=True)
                embed.add_field(name="Research and Development", value=the_income_info['ResearchAndDevelopment'], inline=False)
                embed.add_field(name="OperatingExpenses", value=the_income_info['OperatingExpenses'], inline=True)
                embed.add_field(name="Investment Income Net", value=the_income_info['InvestmentIncomeNet'], inline=True)
                embed.add_field(name="Net Interest Income", value=the_income_info['NetInterestIncome'], inline=True)
                embed.add_field(name="Interest Income", value=the_income_info['InterestIncome'], inline=True)
                embed.add_field(name="Interest Expense", value=the_income_info['InterestExpense'], inline=True)
                embed.add_field(name="Non Interest Income", value=the_income_info['NonInterestIncome'], inline=True)   
                embed.add_field(name="Other Non Operating Income", value=the_income_info['OtherNonOperatingIncome'], inline=True)
                embed.add_field(name="Depreciation", value=the_income_info['Depreciation'], inline=True)
                embed.add_field(name="Depreciation and Amortization", value=the_income_info['DepreciationAndAmortization'], inline=True)
                embed.add_field(name="Income Before Tax", value=the_income_info['IncomeBeforeTax'], inline=True)
                embed.add_field(name="Income Tax Expense", value=the_income_info['IncomeTaxExpense"'], inline=True)
                embed.add_field(name="Interest and Debt Expense", value=the_income_info['InterestandDebtExpense"'], inline=True)
                embed.add_field(name="Net Income from Continuing Operations", value=the_income_info['NetIncomeFromContinuingOperations'], inline=True)
                embed.add_field(name="Comprehensive Income Net of Tax", value=the_income_info['ComprehensiveIncomeNetOfTax'], inline=True)
                embed.add_field(name="ebit", value=the_income_info['Ebit'], inline=True)
                embed.add_field(name="ebitda", value=the_income_info['Ebitda'], inline=True)
                embed.add_field(name="Net Income", value=the_income_info['NetIncome'], inline=True)
              
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve stock data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
    
def setup(client):
    client.add_cog(IncomeStatement(client))
