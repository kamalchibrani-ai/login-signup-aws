import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key, Attr
from streamlit_extras.switch_page_button import switch_page

import os
from dotenv import load_dotenv
load_dotenv('.env')
YOUR_ACCESS_KEY = os.getenv('aws_access_key_id')
YOUR_SECRET_KEY = os.getenv('aws_secret_access_key')

@st.cache_resource
def get_resourse():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=YOUR_ACCESS_KEY,
        aws_secret_access_key=YOUR_SECRET_KEY,
        region_name='eu-west-2' # replace with your preferred region
    )
    return dynamodb

dynamodb = get_resourse()

table = dynamodb.Table('users')

def signup():
    # st.session_state['authenticated'] = False
    username = st.text_input("Username",key='signup_username')
    password = st.text_input("Password", type="password",key='signup_password')
    email = st.text_input("Email",key='signup_email')
    if st.button("Sign up"):
        response = table.put_item(
            Item={
                'username': username,
                'password': password,
                'email': email
            }
        )
        if response.get('ResponseMetadata')['HTTPStatusCode'] == 200:
            st.success("You have successfully signed up.")
            st.info("Please log in to your account.")


def login():
    username = st.text_input("Username",key='login_username')
    password = st.text_input("Password", type="password",key='login_password')
    if st.button("Login"):
        response = table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        items = response['Items']
        print(items)
        if items:
            if items[0]['password'] == password:
                st.success("You have successfully logged in.")
                st.session_state['username'] = username
                st.session_state['authenticated'] = True
                with st.sidebar:
                    # username = st.session_state['username']
                    st.write(f"Hello {username}")
                    logout()
                    switch_page('page1')

            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

def logout():
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None



def main():
    st.title("Login/Sign up App")
    tab1 , tab2 = st.tabs(['Login', 'Sign up'])
    with tab1:
        login()
    with tab2:
        signup()

if __name__ == '__main__':
    main()




