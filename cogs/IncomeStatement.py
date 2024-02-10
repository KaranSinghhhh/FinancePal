import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pagination View Class
class PaginationView(nextcord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0

    @nextcord.ui.button(label="Previous", style=nextcord.ButtonStyle.grey)
    async def previous_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page])

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.grey)
    async def next_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page])

# Dropdown Select Class
class Dropdown(nextcord.ui.Select):
    def __init__(self, annual_reports, interaction: Interaction, cog, logo_url):
        super().__init__(placeholder="Choose a Fiscal Date", min_values=1, max_values=1, 
                         options=[nextcord.SelectOption(label=report['fiscalDateEnding']) for report in annual_reports])
        self.annual_reports = annual_reports
        self.interaction = interaction
        self.cog = cog
        self.logo_url = logo_url

    async def callback(self, interaction: Interaction):
        selected_date = self.values[0]
        selected_report = next((report for report in self.annual_reports if report['fiscalDateEnding'] == selected_date), None)
        if selected_report:
            paginated_embeds = self.cog.create_paginated_embeds_for_report(selected_report, self.logo_url)
            view = PaginationView(paginated_embeds)
            await interaction.response.edit_message(content="Here is the income statement:", embed=paginated_embeds[0], view=view)

# Dropdown View Class
class DropdownView(nextcord.ui.View):
    def __init__(self, annual_reports, interaction: Interaction, cog, logo_url):
        super().__init__()
        self.add_item(Dropdown(annual_reports, interaction, cog, logo_url))

# Main Cog Class
class CompanyInfoTest(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')

    async def fetch_income_statement_data(self, symbol):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('annualReports', [])
        return []

    def fetch_logo_image_url(self, symbol):
        api_key = os.getenv('API_NINJAS_KEY')
        api_url = f'https://api.api-ninjas.com/v1/logo?name={symbol}'
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        if response.status_code == 200 and response.json():
            data = response.json()
            if 'image' in data[0]:
                return data[0]['image']
        return None

    def get_company_name_from_ticker(self, symbol):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        endpoint = 'https://www.alphavantage.co/query'
        params = {'function': 'SYMBOL_SEARCH', 'keywords': symbol, 'apikey': api_key}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200 and response.json():
            data = response.json()
            if 'bestMatches' in data and data['bestMatches']:
                full_name = data['bestMatches'][0]['2. name']
                return full_name.split(' ')[0]  # Assuming the company name is the first part
        return None

    '''
    def create_paginated_embeds_for_report(self, report, logo_url):
        embeds = []
        items = list(report.items())
        items_per_page = 13

        for i in range(0, len(items), items_per_page):
            embed = nextcord.Embed(title=f"Income Statement for {report['fiscalDateEnding']}",
                                   description=f"Data from {datetime.now().strftime('%Y-%m-%d')}")
            for key, value in items[i:i+items_per_page]:
                embed.add_field(name=key, value=value, inline=False)
            if logo_url:
                embed.set_thumbnail(url=logo_url)
            embed.set_footer(text="Data provided by FinancePal Bot")
            embeds.append(embed)
        return embeds
    '''
    
    def create_paginated_embeds_for_report(self, the_income_info, logo_url):
        embeds = []

        # Page 1
        embed1 = nextcord.Embed(title=f"Income Statement for {the_income_info['fiscalDateEnding']}",
                                description=f"Data from {datetime.now().strftime('%Y-%m-%d')}")
        # First page fields, corrected for case sensitivity and exact spelling
        embed1.add_field(name="Reported Currency", value=the_income_info.get('reportedCurrency', 'N/A'), inline=True)
        embed1.add_field(name="Gross Profit", value=f"${the_income_info.get('grossProfit', 'N/A')}", inline=True)
        embed1.add_field(name="Total Revenue", value=the_income_info.get('totalRevenue', 'N/A'), inline=False)
        embed1.add_field(name="Cost Of Revenue", value=the_income_info.get('costOfRevenue', 'N/A'), inline=False)
        embed1.add_field(name="Cost of Goods and Services Sold", value=the_income_info.get('costofGoodsAndServicesSold', 'N/A'), inline=False)
        embed1.add_field(name="Operating Income", value=the_income_info.get('operatingIncome', 'N/A'), inline=True)
        embed1.add_field(name="Selling General and Administrative", value=the_income_info.get('sellingGeneralAndAdministrative', 'N/A'), inline=True)
        embed1.add_field(name="Research and Development", value=the_income_info.get('researchAndDevelopment', 'N/A'), inline=False)
        embed1.add_field(name="Operating Expenses", value=the_income_info.get('operatingExpenses', 'N/A'), inline=True)
        embed1.add_field(name="Investment Income Net", value=the_income_info.get('investmentIncomeNet', 'N/A'), inline=True)
        embed1.add_field(name="Net Interest Income", value=the_income_info.get('netInterestIncome', 'N/A'), inline=True)
        embed1.add_field(name="Interest Income", value=the_income_info.get('interestIncome', 'N/A'), inline=True)

        if logo_url:
            embed1.set_thumbnail(url=logo_url)
        embed1.set_footer(text="Data provided by FinancePal Bot")
        embeds.append(embed1)

        # Page 2
        embed2 = nextcord.Embed(title=f"Income Statement for {the_income_info['fiscalDateEnding']}",
                                description=f"Continued...")
        # Second page fields, corrected for case sensitivity and exact spelling
        embed2.add_field(name="Interest Expense", value=the_income_info.get('interestExpense', 'N/A'), inline=True)
        embed2.add_field(name="Non Interest Income", value=the_income_info.get('nonInterestIncome', 'N/A'), inline=True)
        embed2.add_field(name="Other Non Operating Income", value=the_income_info.get('otherNonOperatingIncome', 'N/A'), inline=True)
        embed2.add_field(name="Depreciation", value=the_income_info.get('depreciation', 'N/A'), inline=True)
        embed2.add_field(name="Depreciation and Amortization", value=the_income_info.get('depreciationAndAmortization', 'N/A'), inline=True)
        embed2.add_field(name="Income Before Tax", value=the_income_info.get('incomeBeforeTax', 'N/A'), inline=True)
        embed2.add_field(name="Income Tax Expense", value=the_income_info.get('incomeTaxExpense', 'N/A'), inline=True)
        embed2.add_field(name="Interest and Debt Expense", value=the_income_info.get('interestAndDebtExpense', 'N/A'), inline=True)
        embed2.add_field(name="Net Income from Continuing Operations", value=the_income_info.get('netIncomeFromContinuingOperations', 'N/A'), inline=True)
        embed2.add_field(name="Comprehensive Income Net of Tax", value=the_income_info.get('comprehensiveIncomeNetOfTax', 'N/A'), inline=True)
        embed2.add_field(name="ebit", value=the_income_info.get('ebit', 'N/A'), inline=True)
        embed2.add_field(name="ebitda", value=the_income_info.get('ebitda', 'N/A'), inline=True)
        embed2.add_field(name="Net Income", value=the_income_info.get('netIncome', 'N/A'), inline=True)

        if logo_url:
            embed2.set_thumbnail(url=logo_url)
        embed2.set_footer(text="Data provided by FinancePal Bot")
        embeds.append(embed2)

        return embeds


    @nextcord.slash_command(name="income-statement", description="Gets the income statement for a selected fiscal date", guild_ids=[int(os.getenv('TEST_SERVER_ID'))] )
    async def the_income_statement(self, interaction: Interaction, symbol :str):
        annual_reports = await self.fetch_income_statement_data(symbol)
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
        if annual_reports:
            view = DropdownView(annual_reports, interaction, self, logo_url)
            await interaction.response.send_message("Select a fiscal date:", view=view)
        else:
            await interaction.response.send_message("No income statement data available for this symbol.", ephemeral=True)

def setup(client):
    client.add_cog(CompanyInfoTest(client))
