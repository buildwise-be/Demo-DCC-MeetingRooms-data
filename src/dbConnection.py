# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from datetime import datetime
from entityType import EntityType
import configparser

class InsertDeleteEntity(object):
    def __init__(self):
        # Read configuration from config file
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.access_key = config['Settings']['access_key']
        self.endpoint_suffix = config['Settings']['endpoint_suffix']
        self.account_name = config['Settings']['account_name']
        self.endpoint = f"{self.account_name}.table.{self.endpoint_suffix}"
        self.connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.access_key};EndpointSuffix={self.endpoint_suffix}"
        self.table_name = config['Settings']['table_name']

        self.entity: EntityType = {
            "PartitionKey": "BWZ",
            "RowKey": str(datetime.now()) + "MR_1",
            "room": 1,
            "start_time": datetime.now(),
            "organizer": "John",
            "title": "MyCoolMeeting"
        }
    
    def __init__(self, entity: EntityType):
        # Read configuration from config file
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.access_key = config['Settings']['access_key']
        self.endpoint_suffix = config['Settings']['endpoint_suffix']
        self.account_name = config['Settings']['account_name']
        self.endpoint = f"{self.account_name}.table.{self.endpoint_suffix}"
        self.connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.access_key};EndpointSuffix={self.endpoint_suffix}"
        self.table_name = config['Settings']['table_name']

        self.entity: EntityType = entity

    
    def create_entity(self):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceExistsError, HttpResponseError

        with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:

            # Create a table in case it does not already exist
            try:
                table_client.create_table()
            except HttpResponseError:
                print("Table already exists")

            # [START create_entity]
            try:
                resp = table_client.create_entity(entity=self.entity)
                print("Inserting " + str(self.entity))
            except ResourceExistsError:
                print("Entity already exists")
        # [END create_entity]

    def delete_entity(self):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceExistsError
        from azure.core.credentials import AzureNamedKeyCredential

        credential = AzureNamedKeyCredential(self.account_name, self.access_key)
        with TableClient(endpoint=self.endpoint, table_name=self.table_name, credential=credential) as table_client:

            # Create entity to delete (to showcase etag)
            try:
                table_client.create_entity(entity=self.entity)
            except ResourceExistsError:
                print("Entity already exists!")

            # [START delete_entity]
            table_client.delete_entity(row_key=self.entity["RowKey"], partition_key=self.entity["PartitionKey"])
            print("Successfully deleted!")
            # [END delete_entity]