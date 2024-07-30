# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:24:46 2024

@author: aca
"""

from webScraper import MeetingRoomScraper
from dbConnection import InsertDeleteEntity
import configparser
from entityType import EntityType

# Read configuration from config file
config = configparser.ConfigParser()
config.read('config.ini')

# Get URL from configuration
URL = config['Settings']['url']
CHROMEPATH = config['Settings']['chromeDriverPath']

scraper = MeetingRoomScraper(driver_path=CHROMEPATH, url=URL)
entities = scraper.scrape()

for e in entities:
    ide = InsertDeleteEntity(entity=e)
    ide.create_entity()

def print_table_contents(table_name: str, conn_str: str):
    from azure.data.tables import TableClient
    my_filter = "PartitionKey eq 'BWZ' and room eq '3'"
    table_client = TableClient.from_connection_string(conn_str, table_name)
    entities = table_client.query_entities(my_filter)
    for entity in entities:
        for key in entity.keys():
            print(f"Key: {key}, Value: {entity[key]}")

#print_table_contents(config['Settings']['table_name'], connection_string)