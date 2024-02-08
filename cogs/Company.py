import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import SlashOption, ui
import json
from nextcord.ext import commands
from nextcord import Interaction
from dotenv import load_dotenv
import os

load_dotenv()

class Company(commands.Cog):
    def __init__ (self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
    
    
    def get_company_info(self, symbol):
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            
            company_values = {
                "name": data['Name'],
                "description": data['Description'],
                "country": data['Country'],
                "industry": data['Industry'],
                "sector": data['Sector'],
                "marketcap": data['MarketCapitalization'],
                "PEratio" : data['PERatio'],
                "DividendPerShare": data['DividendPerShare'],
                "DividendYield": data['DividendYield'],
                "EPS": data['EPS']
                
            }
            return company_values
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    @nextcord.slash_command(name="company-info", description="Gets company info", guild_ids=[testServerId])
    async def company_info(self, interaction: Interaction, symbol: str):
        the_company_info = self.get_company_info(symbol)
        try: 
            if the_company_info:
                embed = nextcord.Embed(title=f"{symbol}", description="Info for Ticker:", color=0x4dff4d)
                embed.add_field(name="Name", value=the_company_info['name'], inline=False)
                embed.add_field(name="country", value=the_company_info['country'], inline=False)
                embed.add_field(name="industry", value=the_company_info['industry'], inline=False)
                embed.add_field(name="description", value=the_company_info['description'], inline=False)
                embed.add_field(name="Sector", value=the_company_info['sector'], inline=False)
                embed.add_field(name="Market Cap", value=the_company_info['marketcap'], inline=False)
                embed.add_field(name="P/E Ratio", value=the_company_info['PEratio'], inline=False)
                embed.add_field(name="Dividend Per Share", value=the_company_info['DividendPerShare'], inline=False)
                embed.add_field(name="EPS", value=the_company_info['EPS'], inline=False)
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve stock data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
    
    '''
    def get_income_statement(self, symbol, fiscal_dates):
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data=response.json()
                
            fiscal_dates = []
                
            for report in data['annualReports']:
                fiscal_date = report['fiscalDateEnding']
                print(fiscal_date)
                fiscal_dates.append(fiscal_date)
                
            for i in fiscal_dates:
                for report in data['annualReports']:
                    if report['fiscalDateEnding'] == i:
                        fiscal_date_values = {
                            "ReportedCurrency": report['reportedCurrency'],
                            "GrossProfit": report['grossProfit'],
                            "TotalRevenue": report['totalRevenue'],
                            "CostOfRevenue": report['costOfRevene']
                        }
                        return fiscal_date_values
                    
            print("No Matching fiscal date found")
            return None
                
                
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        '''
        

    def get_income_statement(self, symbol, fiscal_dates):
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data=response.json()
                    
                fiscal_dates = []
                    
                for report in data['annualReports']:
                    fiscal_date = report['fiscalDateEnding']
                    print(fiscal_date)
                    fiscal_dates.append(fiscal_date)
                    
                for i in fiscal_dates:
                    for report in data['annualReports']:
                        if report['fiscalDateEnding'] == i:
                            fiscal_date_values = {
                                "ReportedCurrency": report['reportedCurrency'],
                                "GrossProfit": report['grossProfit'],
                                "TotalRevenue": report['totalRevenue'],
                                "CostOfRevenue": report['costOfRevene']
                            }
                            return fiscal_date_values
                class Dropdown(nextcord.ui.Select):
                    def __init__(self):
                        selectOptions = [nextcord.SelectOption(label=date) for date in fiscal_dates]
                        super().__init__(placeholder="Fiscal Date Options", min_values = 1, max_values=1, options = selectOptions)

                    async def callback(self, interaction: Interaction):
                        selected_date = self.values[0]
                        # Here, implement the logic based on the selected date.
                        # For example, sending a message based on the selected date.
                        await interaction.response.send_message(f"Income statement for Fiscal Date: {selected_date}")

                class DropdownView(nextcord.ui.View):
                    def __init__(self, fiscal_dates):
                        super().__init__()
                        self.add_item(Dropdown(fiscal_dates))
                                        
               
                print("No Matching fiscal date found")
                
                
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                return None
          
    @nextcord.slash_command(name="income-statement", description="Gets the latest income statement", guild_ids=[testServerId])
    async def income_statement(self, interaction: Interaction, symbol: str, fiscal_dates: get_income_statement()):
        income_statement_data = self.get_income_statement(symbol)
        
        try:
            if income_statement_data:
                
                embed = nextcord.Embed(title=f"{symbol}", description="Income Statement info for Ticker:", color=0x4dff4d)
                embed.add_field(name="Reported Currency", value=income_statement_data['ReportedCurrency'], inline=False)
                embed.add_field(name="Gross Profit", value=income_statement_data['GrossProfit'], inline=False)
                embed.add_field(name="Total Revenue", value=income_statement_data['TotalRevenue'], inline=False)
                embed.add_field(name="Total Revenue", value=income_statement_data['CostOfRevenue'], inline=False)
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Income Statement information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve income statement data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}") 
        
    
    
        
        
        
    
            
        
    
                    
                    
                

    
   
    ##############################
    '''
    def get_latest_income_statement(self, symbol):
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(json.dumps(data, indent=4))
            
            
            latest_report = data['annualReports'][0] 
            
            income_statement_values = {
                "FiscalDateEnding": latest_report['fiscalDateEnding'],
                "ReportedCurrency": latest_report['reportedCurrency'],
                "GrossProfit": latest_report['grossProfit']
            }
            return income_statement_values
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
            
    @nextcord.slash_command(name="income-statement", description="Gets the latest income statement", guild_ids=[testServerId])
    async def income_statement(self, interaction: Interaction, symbol: str):
        income_statement_data = self.get_latest_income_statement(symbol)
        try:
            if income_statement_data:
                embed = nextcord.Embed(title=f"{symbol}", description="Income Statement info for Ticker:", color=0x4dff4d)
                embed.add_field(name="Fiscal Date Ending", value=income_statement_data['FiscalDateEnding'], inline=False)
                embed.add_field(name="Reported Currency", value=income_statement_data['ReportedCurrency'], inline=False)
                embed.add_field(name="GrossProfit", value=income_statement_data['GrossProfit'], inline=False)
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Income Statement information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve income statement data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}") 
    ''' 
    #############################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    def get_latest_income_statement(self, symbol):
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            latest_report = data['annualReports'][0] 
            return latest_report
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    @nextcord.slash_command(name="income-statement", description="Gets the latest income statement", guild_ids=[testServerId])
    async def income_statement(self, interaction: Interaction, symbol: str):
        income_statement_data = self.get_latest_income_statement(symbol)
        try:
            if income_statement_data:
                embed = nextcord.Embed(title=f"Income Statement for {symbol}", description="Latest Fiscal Date", color=0x4dff4d)
                count = 0
                for key, value in income_statement_data.items():
                    if count < 25:
                        embed.add_field(name=key.capitalize(), value=value, inline=False)
                        count += 1
                    else:
                        break
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Failed to retrieve income statement data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
    '''
 
            
def setup(client):
    client.add_cog(Company(client))

   