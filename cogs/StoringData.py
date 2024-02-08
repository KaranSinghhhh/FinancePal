import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import member
from nextcord.ext.commands import has_permissions, MissingPermissions
import requests
import json
import os
from json import loads
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class StoreData(commands.Cog):
    def __init__ (self, client):
        self.client = client
        
    testServerId = os.getenv('TEST_SERVER_ID')
    
    @nextcord.slash_command(name = "store-info", description ="Store some data from a user into a database", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def store_info(self, interaction: Interaction, message:str):
        
        guild = interaction.guild.id
        
        try:
            connection = mysql.connector.connect(host='localhost', 
                                                 database="discord_bot", 
                                                 user="root", 
                                                 password="")
            
            mysql_create_Table_Query = """CREATE TABLE DB_""" + str(guild) + """(
                                                Id int(11) NOT NULL AUTO_INCREMENT,
                                                User varchar(250) NOT NULL,
                                                Message varchar(5000) NOT NULL,
                                                PRIMARY KEY(Id))"""
                                                
            cursor = connection.cursor()
            result = cursor.execute(mysql_create_Table_Query)
            print("Guild (" + str(guild) + ") Table has been created succesfully")
            
        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
            
        finally:
            if connection.is_connected():
                table = "DB_" + str(guild)
                
            mySql_Insert_Row_Query = "INSERT INTO " + table + " (User, Message) VALUES (%s, %s)"
            mySql_Insert_Row_values = (str(interaction.user), message)
            
            cursor.execute(mySql_Insert_Row_Query, mySql_Insert_Row_values)
            connection.commit()
            
            await interaction.response.send_message("I have stored your message for you!")

            cursor.close()
            connection.close()
            print("Mysql connection has been closed")
            
    @nextcord.slash_command(name = "retrive-info", description ="Retrieves some data that a user stored into a database", guild_ids=[int(os.getenv('TEST_SERVER_ID'))])
    async def retrieve_info(self, interaction: Interaction, message:str):
        guild = interaction.guild.id
        table = "DB_" + str(guild)
        
        try:
            connection = mysql.connector.connect(host='localhost', 
                                                 database="discord_bot", 
                                                 user="root", 
                                                 password="")
        
            cursor = connection.cursor()
            
            sql_select_query = "SELECT * from" + table + "where user like'"+ str(interaction.user) +"'" 
            
            cursor.execute(sql_select_query)
            
            record = cursor.fetchall()
            
            Received_Data = []
            
            for row in record:
                Received_Data.append({"Id": str(row[0]), "Message": str(row[2])})
                
            await interaction.response.send_message("All Stored Data: \n \n" + json.dumps(Received_Data, indent=1))

        except mysql.connector.Error as error:
            print("Failed to get record from MySQL: table: {}".format(error))
            
        finally:
            if connection.is_connected:
                cursor.close()
                connection.close()
                print("MySQL connection is closed ")
                
    
def setup(client):
    client.add_cog(StoreData(client))
