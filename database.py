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