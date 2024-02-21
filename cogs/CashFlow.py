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
        
    @nextcord.ui.button(label="Previous", style= nextcord.Button.style.grey)
    async def previous_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed = self.embeds[self.current_page])

    @nextcord.ui.button(label = "next", style= nextcord.Button.style.grey)
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

    async def fetch_income_statement_data(self, symbol):
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