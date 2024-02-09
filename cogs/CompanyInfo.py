import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import SlashOption, ui
import json
from datetime import datetime
from nextcord.ext import commands
from nextcord import Interaction

from dotenv import load_dotenv
import os

load_dotenv()


class PaginationView(nextcord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0

    @nextcord.ui.button(label="Previous", style=nextcord.ButtonStyle.grey)
    async def previous_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page])

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.grey)
    async def next_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page])




class CompanyInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')
    
    
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
        
    @nextcord.slash_command(name="company-info", description="Gets company info", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def company_info(self, interaction: Interaction, symbol: str):
        the_company_info = self.get_company_info(symbol)
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
       
        
        try: 
            if the_company_info:
                bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
                
                
                embed = nextcord.Embed(title=f"{symbol} Stock", url=bloomberg_url, description="Info for Ticker:", color=0x4dff4d)
                
                    
                if logo_url and logo_url.startswith(("http://", "https://")):
                    embed.set_thumbnail(url=logo_url)
                    
                current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
                embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
                
                finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
                embed.set_author(name="FinancePal", icon_url=finance_pal_url)
                
                embed.add_field(name="Name", value=the_company_info['name'], inline=True)
                embed.add_field(name="Country", value=the_company_info['country'], inline=True)
                embed.add_field(name="Industry", value=the_company_info['industry'], inline=False)
                embed.add_field(name="Sector", value=the_company_info['sector'], inline=False)
                embed.add_field(name="Description", value=the_company_info['description'], inline=False)
                embed.add_field(name="Market Cap", value=the_company_info['marketcap'], inline=True)
                embed.add_field(name="P/E Ratio", value=the_company_info['PEratio'], inline=True)
                embed.add_field(name="Dividend Per Share", value=the_company_info['DividendPerShare'], inline=False)
                embed.add_field(name="EPS", value=the_company_info['EPS'], inline=True)
                
                
                
                
                await interaction.user.send(embed=embed)
                await interaction.response.send_message(f"Stock information sent to your DMs.", ephemeral=False)
            else:
                await interaction.response.send_message("Failed to retrieve stock data.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")
    

    async def fetch_income_statement_data(self, symbol):
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        response = requests.get(url)
        data = response.json()
        return data.get('annualReports', [])

    class Dropdown(nextcord.ui.Select):
        def __init__(self, annual_reports, interaction: Interaction, cog, logo_url):
            self.annual_reports = annual_reports
            self.interaction = interaction
            self.cog = cog
            self.logo_url = logo_url
            options = [nextcord.SelectOption(label=report['fiscalDateEnding']) for report in annual_reports]
            super().__init__(placeholder="Choose a Fiscal Date", min_values=1, max_values=1, options=options)


        async def callback(self, interaction: Interaction):
            selected_date = self.values[0]
            selected_report = next((report for report in self.annual_reports if report['fiscalDateEnding'] == selected_date), None)

            if selected_report:
                print(f"Selected report symbol: {selected_report.get('symbol')}")
                
                # Fetch the logo URL
                symbol = selected_report.get('symbol', '')
                logo_url = self.cog.fetch_logo_image_url(symbol)

                

                # Create paginated embeds
                paginated_embeds = self.cog.create_paginated_embeds_for_report(selected_report, selected_report.get('symbol', ''), self.logo_url)
                view = PaginationView(paginated_embeds)
                await interaction.response.edit_message(content="Here is the income statement:", embed=paginated_embeds[0], view=view)
            else:
                await interaction.response.send_message("No data available for the selected fiscal date.", ephemeral=True)




    class DropdownView(nextcord.ui.View):
        def __init__(self, annual_reports, interaction: Interaction, cog, logo_url):
            super().__init__()
            self.cog = cog
            self.logo_url = logo_url
            self.add_item(CompanyInfo.Dropdown(annual_reports, interaction, cog, logo_url))

    
    def create_paginated_embeds_for_report(self, report, symbol, logo_url):
        bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
        finance_pal_url = "https://styles.redditmedia.com/t5_3nimn/styles/communityIcon_cho9chd8ug431.jpg?format=pjpg&s=e4500f8195a317b675dabd11d245047ac400aa8b"
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')

        first_page_items = list(report.items())[:10]
        second_page_items = list(report.items())[10:20]
        
       

        first_page_embed = nextcord.Embed(title=f"Income Statement for {report['fiscalDateEnding']}", description="Page 1")
        for key, value in first_page_items:
            first_page_embed.add_field(name=key.capitalize(), value=value, inline=False)

        second_page_embed = nextcord.Embed(title=f"Income Statement for {report['fiscalDateEnding']}", description="Page 2")
        for key, value in second_page_items:
            second_page_embed.add_field(name=key.capitalize(), value=value, inline=False)

        # common elements for each embed
        for embed in [first_page_embed, second_page_embed]:
            if logo_url and logo_url.startswith(("http://", "https://")):
                embed.set_thumbnail(url=logo_url)
            embed.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
            embed.set_author(name="FinancePal", icon_url=finance_pal_url)
            embed.url = bloomberg_url
            
        print(f"Setting thumbnail to: {logo_url}")  # This line should just be for debugging, remove after confirming it works

        return [first_page_embed, second_page_embed]
        
      
    @nextcord.slash_command(name="get-income-statement", description="Gets the income statement for a selected fiscal date", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def the_income_statement(self, interaction: Interaction, symbol: str):
        annual_reports = await self.fetch_income_statement_data(symbol)
            
        # Fetch the full company name from the symbol
        company_name = self.get_company_name_from_ticker(symbol)
            
        # Fetch the logo using the full company name if available, otherwise use the symbol
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
        print(f"Fetched logo URL for {symbol} (company name: {company_name}): {logo_url}")  # Debugging line
            
        if annual_reports:
        # Pass the logo_url to the DropdownView
            view = self.DropdownView(annual_reports, interaction, self, logo_url)
            await interaction.response.send_message("Select a fiscal date:", view=view)
        else:
            await interaction.response.send_message("No income statement data available for this symbol.")



            
 
            
    async def get_cash_flow_data(self, symbol):
        url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('annualReports', [])
    
    class CashFlowDropdown(nextcord.ui.Select):
        def __init__(self, cash_flow_annual_reports, interaction: Interaction):
            self.cash_flow_annual_reports = cash_flow_annual_reports
            self.interaction = interaction
            options = [nextcord.SelectOption(label=report['fiscalDateEnding']) for report in cash_flow_annual_reports]
            super().__init__(placeholder="Choose a Fiscal Date", min_values=1, max_values=1, options=options)

        async def callback(self, interaction: Interaction):
            selected_date = self.values[0]
            for report in self.cash_flow_annual_reports:
                if report['fiscalDateEnding'] == selected_date:
                    embed = nextcord.Embed(title=f"Income Statement for {selected_date}", color=0x4dff4d)
                    
                    cash_flow_last_25_items = list(report.items())[-25:]
                    
                    for key, value in cash_flow_last_25_items:
                        embed.add_field(name=key.capitalize(), value=value, inline=False)


                    await interaction.user.send(embed=embed)
                    await interaction.response.send_message(f"Income Statement information sent to your DMs.",)
                    return
                
    class CashFlowDropdownView(nextcord.ui.View):
        def __init__(self, cash_flow_annual_reports, interaction: Interaction):
            super().__init__()
            self.add_item(CompanyInfo.CashFlowDropdown(cash_flow_annual_reports, interaction))        
                
                
    @nextcord.slash_command(name="get-cash-flow-statement", description="Gets the cash flow statement for a selected fiscal date", guild_ids=[testServerId])
    async def the_cash_flow_statement(self, interaction:Interaction, symbol: str):
        cash_flow_annual_reports = await self.get_cash_flow_data(symbol)  # Corrected this line
        if cash_flow_annual_reports:
            view = CompanyInfo.CashFlowDropdownView(cash_flow_annual_reports, interaction)
            await interaction.response.send_message("Select a fiscal date for the cash flow statement:", view=view)
        else:
            await interaction.response.send_message("No cash flow statement data available for this symbol.")
            
    def get_balance_sheet(self, symbol):
        url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('annualReports', [])

    class BalanceSheetDropdown(nextcord.ui.Select):
        def __init__(self, balance_sheet_reports, interaction: Interaction):
            self.balance_sheet_reports = balance_sheet_reports
            self.interaction = interaction
            options = [nextcord.SelectOption(label=report['fiscalDateEnding']) for report in balance_sheet_reports]
            super().__init__(placeholder="Choose a Fiscal Date", min_values=1, max_values=1, options=options)
            
        async def callback(self, interaction: Interaction):
                selected_date = self.values[0]
                for report in self.balance_sheet_reports:
                    if report['fiscalDateEnding'] == selected_date:
                        embed = nextcord.Embed(title=f"Balance Sheet for {selected_date}", color=0x4dff4d)
                        
                        balance_sheet_last_25_items = list(report.items())[-25:]
                        
                        for key, value in balance_sheet_last_25_items:
                            embed.add_field(name=key.capitalize(), value=value, inline=False)


                        await interaction.user.send(embed=embed)
                        await interaction.response.send_message(f"Balance Sheet Statement information sent to your DMs.",)
                        return
                
    class BalanceSheetDropdownView(nextcord.ui.View):
        def __init__(self, balance_sheet_reports, interaction: Interaction):
            super().__init__()
            self.add_item(CompanyInfo.BalanceSheetDropdown(balance_sheet_reports, interaction))        
                
    @nextcord.slash_command(name="get-balance-sheet-statement", description="Gets the balance sheet statement for a selected fiscal date", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def the_balance_sheet_statement(self, interaction:Interaction, symbol: str):
        cash_flow_annual_reports = await self.get_balance_sheet(symbol)  # Corrected this line
        if cash_flow_annual_reports:
            view = CompanyInfo.BalanceSheetDropdownView(cash_flow_annual_reports, interaction)
            await interaction.response.send_message("Select a fiscal date for the Balance Sheet statement:", view=view)
        else:
            await interaction.response.send_message("No Balance Sheet statement data available for this symbol.")
            


def setup(client):
    client.add_cog(CompanyInfo(client))
        

   