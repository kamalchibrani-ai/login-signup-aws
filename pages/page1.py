import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import logout_button_sidebar,switch_page_if_auth_isFalse
from database import fetch_data,get_table,get_resourse
from decimal import Decimal
if st.session_state['user_profile'] == True:
    switch_page('user_profile')
switch_page_if_auth_isFalse()
logout_button_sidebar()

dynamodb = get_resourse()
table = get_table('user_profile',dynamodb)


def format_data(data):
    formatted_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            formatted_data[k] = format_data(v)
        elif isinstance(v, list):
            formatted_data[k] = ', '.join(v)
        elif isinstance(v, Decimal):
            formatted_data[k] = float(v)
        else:
            formatted_data[k] = v
    return formatted_data


if st.session_state['authenticated']:
    # data = fetch_data_from_dynamodb(table, 'username',st.session_state['username'])
    # print(data)
    user_item = fetch_data(table,st.session_state['username'],dynamodb)
    print(user_item)
    formatted_data = format_data(user_item)
    print(formatted_data)
    # Convert Decimal to float for better formatting


