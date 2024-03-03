import requests
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import os
from datetime import datetime
from dotenv import load_dotenv

#Load environment variable
load_dotenv()

#Pagination View Class
class PaginationView(nextcord.ui.View):
    def __init__(self,embeds):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        
    @nextcord.ui.button(label="Previous", style=nextcord.ButtonStyle.grey)
    async def previous_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed = self.embeds[self.current_page])

    @nextcord.ui.button(label = "next", style= nextcord.ButtonStyle.grey)
    async def next_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed = self.embeds[self.current_page])
            
            
#Dropdown Select Class
class Dropdown(nextcord.ui.Select):
    def __init__(self, symbol, annual_reports, interaction: Interaction, cog, logo_url):
        super().__init__(placeholder="Choose a Fiscal Date",min_values=1, max_values=1,
                         options=[nextcord.SelectOption(label=report['fiscalDateEnding']) for report in annual_reports])
        self.symbol=symbol
        self.annual_reports=annual_reports
        self.interaction = interaction
        self.cog=cog
        self.logo_url = logo_url
        
    async def callback(self, interaction: Interaction):
        selected_date = self.values[0]
        selected_report = next((report for report in self.annual_reports if report ['fiscalDateEnding'] == selected_date), None)
        if selected_report:
            paginated_embeds=self.cog.create_paginated_embeds_for_report(self.symbol, selected_report, self.logo_url)
            view = PaginationView(paginated_embeds)
            await interaction.response.edit_message(content="Here is the Cash Flow statement:", embed=paginated_embeds[0], view=view)
            
# Dropdown View Class
class DropdownView(nextcord.ui.View):
    def __init__(self, symbol, annual_reports, interaction: Interaction, cog, logo_url):
        super().__init__()
        self.add_item(Dropdown(symbol, annual_reports, interaction, cog, logo_url))
        
# Main Cog Class
class CashFlow(commands.Cog):
    def __init__(self, client):
        self.client = client
    testServerId = os.getenv('TEST_SERVER_ID')

    async def fetch_cash_flow_statement_data(self, symbol):
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}"
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
    
    def create_paginated_embeds_for_report(self, symbol, the_cash_flow , logo_url):
        embeds = []
        bloomberg_url = f"https://www.bloomberg.com/quote/{symbol}:US"
        # Page 1
        embed1 = nextcord.Embed(title=f"{symbol} Cash Flow Statement", url=bloomberg_url, description=f"Fiscal Report Date: {the_cash_flow['fiscalDateEnding']}", color=0x4dff4d)
        embed1.add_field(name="Operating Cash Flow", value=f"${the_cash_flow.get('operatingCashFlow', 'N/A')}", inline=False)
        embed1.add_field(name="Payments for Operating Activities", value=f"${the_cash_flow.get('paymentsForOperatingActivities', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Operating Activities", value=f"${the_cash_flow.get('proceedsFromOperatingActivities', 'N/A')}", inline=False)
        embed1.add_field(name="Change in Operating Liabilities", value=f"${the_cash_flow.get('changeInOperatingLiabilities', 'N/A')}", inline=False)
        embed1.add_field(name="Change in Operating Assets", value=f"${the_cash_flow.get('changeInOperatingAssets', 'N/A')}", inline=False)
        embed1.add_field(name="Depreciation Depletion and Amortization", value=f"${the_cash_flow.get('depreciationDepletionAndAmortization', 'N/A')}", inline=False)
        embed1.add_field(name="Capital Expenditures", value=f"{the_cash_flow.get('capitalExpenditures', 'N/A')}", inline=False)
        embed1.add_field(name="Change in Receivables", value=f"${the_cash_flow.get('changeInReceivables', 'N/A')}", inline=False)
        embed1.add_field(name="Change in Inventory", value=f"${the_cash_flow.get('changeInInventory', 'N/A')}", inline=False)
        embed1.add_field(name="Cash Flow from Investment", value=f"${the_cash_flow.get('cashflowFromInvestment', 'N/A')}", inline=False)
        embed1.add_field(name="Cash Flow from Financing", value=f"${the_cash_flow.get('cashflowFromFinancing', 'N/A')}", inline=False)
        
        if logo_url:
            embed1.set_thumbnail(url=logo_url)
        
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
        embed1.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
        embeds.append(embed1)
        
        embed2 = nextcord.Embed(title=f"{symbol} Cash Flow Statement", url=bloomberg_url, description=f"Fiscal Report Date: {the_cash_flow['fiscalDateEnding']}", color=0x4dff4d)
        embed1.add_field(name="Proceeds from Payment of Short Term Debt", value=f"${the_cash_flow.get('proceedsFromRepaymentsOfShortTermDebt', 'N/A')}", inline=False)
        embed1.add_field(name="Payments for Repurchase of Common Stock", value=f"${the_cash_flow.get('paymentsForRepurchaseOfCommonStock', 'N/A')}", inline=False)
        embed1.add_field(name="Payments for Repurchase of Equity", value=f"${the_cash_flow.get('paymentsForRepurchaseOfEquity', 'N/A')}", inline=False)
        embed1.add_field(name="Payments for Repurchase of Preferred Stock", value=f"${the_cash_flow.get('paymentsForRepurchaseOfPreferredStock', 'N/A')}", inline=False)
        embed1.add_field(name="Dividend Payout", value=f"${the_cash_flow.get('dividendPayout', 'N/A')}", inline=False)
        embed1.add_field(name="Dividend Payout Common Stock", value=f"${the_cash_flow.get('dividendPayoutCommonStock', 'N/A')}", inline=False)
        embed1.add_field(name="Divident Payout Preferred Stock", value=f"${the_cash_flow.get('dividendPayoutPreferredStock', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Issuance of Common Stock", value=f"${the_cash_flow.get('proceedsFromIssuanceOfCommonStock', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Issuance of Long Term Debt and Capital Securities Net", value=f"${the_cash_flow.get('proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Issuance of Preferred Stock", value=f"${the_cash_flow.get('proceedsFromIssuanceOfPrefferedStock', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Repurchase of Equity ", value=f"${the_cash_flow.get('proceedsFromRepurchaseOfEquity', 'N/A')}", inline=False)
        embed1.add_field(name="Proceeds from Sale of Treasury Stock", value=f"${the_cash_flow.get('proceedsFromSaleOfTreasuryStock', 'N/A')}", inline=False)
        embed1.add_field(name="Change In Cash and Cash Equivalents", value=f"${the_cash_flow.get('changeInCashAndCashEquivalents', 'N/A')}", inline=False)
        embed1.add_field(name="Change In Exchange Rate", value=f"${the_cash_flow.get('changeInExchangeRate', 'N/A')}", inline=False)
        
        
        if logo_url:
            embed2.set_thumbnail(url=logo_url)
        #embed2.set_footer(text="Data provided by FinancePal Bot")
        current_time = datetime.now().strftime('%m/%d/%Y %H:%M %p')
        embed2.set_footer(text=f"Data provided by FinancePal Bot | {current_time}")
        embeds.append(embed2)

        return embeds
          
    
    @nextcord.slash_command(name="cash-flow", description="Gets the Cash Flow Statement for a selected fiscal date", guild_ids=[int(os.getenv('TEST_SERVER_ID'))] )
    async def the_cashflow_statement(self, interaction: Interaction, symbol :str):
        annual_reports = await self.fetch_cash_flow_statement_data(symbol)
        company_name = self.get_company_name_from_ticker(symbol)
        logo_url = self.fetch_logo_image_url(company_name if company_name else symbol)
        if annual_reports:
            view = DropdownView(symbol, annual_reports, interaction, self, logo_url)
            await interaction.response.send_message("Select a fiscal date:", view=view)
        else:
            await interaction.response.send_message("No cash flow statement data available for this symbol.", ephemeral=True)

def setup(client):
    client.add_cog(CashFlow(client))
