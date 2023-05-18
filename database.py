import os
from dotenv import load_dotenv
load_dotenv('.env')
YOUR_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
YOUR_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
import streamlit as st
import boto3

@st.cache_resource
def get_resourse():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=YOUR_ACCESS_KEY,
        aws_secret_access_key=YOUR_SECRET_KEY,
        region_name='eu-west-2' # replace with your preferred region
    )
    return dynamodb



def get_table(table_name,dynamodb):
    table = dynamodb.Table(table_name)
    return table

import boto3

def fetch_data_from_dynamodb(table_name, partition_key_name, partition_key_value):
    # Initialize DynamoDB client
    dynamodb_client = boto3.client('dynamodb')

    # Get table information
    table_description = dynamodb_client.describe_table(TableName=table_name)
    partition_key_type = table_description['Table']['KeySchema'][0]['KeyType']
    partition_key_data_type = table_description['Table']['AttributeDefinitions'][0]['AttributeType']

    # Construct key object
    partition_key = {
        partition_key_name: {
            partition_key_data_type: partition_key_value
        }
    }

    # Fetch data from DynamoDB
    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key=partition_key,
            ConsistentRead=True
        )
        item = response.get('Item')
        if item is None:
            print(f"No item found with partition key value {partition_key_value}")
        else:
            return item
    except Exception as e:
        print(f"Error fetching data from table {table_name}: {e}")

def fetch_data(tablename ,username, dynamodb_client):
    response = tablename.get_item(
        Key={
            'username': username
        }
    )

    if 'Item' in response:
        item = response['Item']
        return item