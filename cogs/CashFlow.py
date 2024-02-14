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