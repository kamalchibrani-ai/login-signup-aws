import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key, Attr
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from streamlit.server.server import Server
from streamlit import session_state
import os
from streamlit_echarts import st_echarts
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT')

@st.cache_resource(allow_output_mutation=True)
def get_resource():
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, endpoint_url=DYNAMODB_ENDPOINT)
    table = dynamodb.Table('users')
    return table

table = get_resource()

def signup():
    st.title('Signup')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    email = st.text_input('Email')
    if st.button('Sign up'):
        if username and password and email:
            response = table.put_item(Item={'username': username, 'password': _CodeHasher().hash(password),
                                             'email': email})
            if response:
                st.success('Successfully signed up! Please login.')
                st.experimental_rerun()
        else:
            st.warning('Please fill all the fields.')

def forgot_password():
    st.title('Forgot Password')
    username = st.text_input('Username')
    email = st.text_input('Email')
    if st.button('Send password reset link'):
        if username and email:
            response = table.scan(FilterExpression=Attr('username').eq(username) & Attr('email').eq(email))
            if response['Items']:
                st.success('A password reset link has been sent to your email.')
                st.experimental_rerun()
            else:
                st.warning('Invalid username or email.')
        else:
            st.warning('Please fill all the fields.')

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username and password:
            response = table.scan(FilterExpression=Attr('username').eq(username))
            if response['Items']:
                if _CodeHasher().verify(password, response['Items'][0]['password']):
                    session_state.username = username
                    st.experimental_set_query_params(username=session_state.username)
                else:
                    st.warning('Incorrect password.')
            else:
                st.warning('Username does not exist.')

def logout():
    del session_state.username
    st.experimental_set_query_params()

def main():
    st.set_page_config(page_title='Login/Signup')

    tabs = ['Login', 'Signup', 'Forgot Password']
    page = st.sidebar.radio('Select a page', tabs)

    if page == 'Login':
        login()
        if 'username' in session_state:
            # switch_page(Server.get_current()._session_info.session.request, '/auth/home')
            pass
    elif page == 'Signup':
        signup()
    elif page == 'Forgot Password':
        forgot_password()