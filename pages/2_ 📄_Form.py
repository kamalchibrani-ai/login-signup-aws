import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from dotenv import load_dotenv
import os
import boto3
from database import get_resourse,get_table,fetch_data_from_dynamodb,fetch_data
load_dotenv('.env')
from utils import switch_page_if_auth_isFalse,logout_button_sidebar,things_with_sidebar
from decimal import Decimal


if st.session_state['user_profile'] == False:
    switch_page('Profile')


switch_page_if_auth_isFalse()
logout_button_sidebar()


st.header('Welcome '+ st.session_state['username'])

dynamodb = get_resourse()
table = get_table('user_profile', dynamodb)



def get_marks():
    marks_10th = Decimal(str(st.number_input('Enter your 10th marks in percentage', min_value=0.0, max_value=100.0, step=0.1, key='marks_10th')))
    marks_12th = Decimal(str(st.number_input('Enter your 12th marks in percentage', min_value=0.0, max_value=100.0, step=0.1, key='marks_12th')))
    return marks_10th, marks_12th

def get_degree_type():
    degree_type = st.radio('Which degree are you interested in pursuing?', ('Bachelors', 'Masters'))
    if degree_type == 'Masters':
        bachelors = Decimal(str(st.number_input('Enter your Bachelors marks in CGPA', min_value=0.0, max_value=10.0, step=0.10, key='bachelors')))
        return degree_type, bachelors
    return degree_type, None

def get_test_scores():
    test_types = ('GRE', 'TOEFL', 'IELTS', 'GMAT', 'SAT', 'ACT', 'LSAT', 'MCAT', 'PCAT', 'DAT', 'OAT', 'Other')
    test_type = st.multiselect('Which standardized tests have you taken or plan to take?', test_types, key='test_type')
    test_scores = {}

    if 'Other' in test_type:
        other_test_name = st.text_input('Enter the name of the test').upper()
        if len(other_test_name) < 0:
            st.error('Please enter the name of the test before entering the score')
    for t in test_type:
        if t != 'Other':
            test_scores[t] = Decimal(str(st.number_input(f'Enter your {t} score', min_value=0.0, max_value=500.0, step=0.1)))
        else:
            if len(other_test_name) > 0:
                if other_test_name not in test_types:
                    other_test_score = st.number_input(f'Enter your {other_test_name} score', min_value=0.0, max_value=500.0, step=0.1)
                    test_scores[other_test_name] = Decimal(str(other_test_score))
                    test_type.remove('Other')
                else:
                    st.error('Test already exists')
            else:
                st.error('Please enter the name of the test before entering the score')
    return test_scores

def get_country_and_field():
    countries = ('USA', 'CANADA', 'UK', 'AUS', 'NEW ZEALAND', 'GERMANY', 'FRANCE', 'SINGAPORE', 'Other')
    country = st.multiselect('Which country/countries do you want to study in?', countries, key='country')

    if 'Other' in country:
        other_country = st.text_input('Enter the name of the country').upper()
        if len(other_country) < 0:
            st.error('Please enter the name of the country before proceeding')
        else:
            if other_country in countries:
                st.error('Country already exists')
            else:
                country.remove('Other')
                country.append(other_country)

    field = st.text_input('What field are you interested in studying?')
    return country, field

# Set page title
# st.title('User Profile')

# Get user input
marks_10th, marks_12th = get_marks()
degree_type, bachelors = get_degree_type()
test_scores = get_test_scores()
country, field = get_country_and_field()

# Save user input
if st.button('Start Conversation',type='primary'):
    user_data = {
        'username': st.session_state['username'],  # Replace with the actual username
        'marks_10th': marks_10th,
        'marks_12th': marks_12th,
        'degree_type': degree_type,
        'bachelors': bachelors,
        'test_scores': test_scores,
        'country': country,
        'field': field
    }

    try:
        table.put_item(Item=user_data)
        print("Successfully inserted user input into the database")
        switch_page('Profile')
        st.session_state.user_profile = False
    except Exception as e:
        print("Error inserting user input into the database")
        print(e)
