import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.no_default_selectbox import selectbox

from utils import logout_button_sidebar,switch_page_if_auth_isFalse,EmailUs
from database import fetch_data,get_table,get_resourse
from decimal import Decimal


switch_page_if_auth_isFalse()
logout_button_sidebar()
EmailUs()

if st.session_state['user_profile'] == False:
    switch_page('Form')



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
    user_item = None
    if user_item is None:
        user_item = fetch_data(table,st.session_state['username'],dynamodb)
        # print(user_item)

    formatted_data = format_data(user_item)
    colored_header(f"Welcome {formatted_data['username']}",color_name='light-blue-70')
    # st.header(f"Welcome {formatted_data['username']}")
    st.title("User Data")
    # # Present the extracted data using Streamlit
    # for key,values in formatted_data.items():
    #     if key == 'test_scores':
    #         for key,value in values.items():
    #             print(key , value)
    #             st.text(f'{key}  {value}')
    #     st.text(f'{key}  {values}')

    def fetch_keys_values(dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                fetch_keys_values(value)# Recursive call for nested dictionaries
                return len(value),value
                # st.metric(key,value)

    col1,col2 = st.columns(2)
    # fetch_keys_values(formatted_data)
    with col1:
        st.subheader(f"Degree Type: {formatted_data['degree_type']}")
        st.subheader(f"Field: {formatted_data['field']}")
        st.subheader(f"Country: {formatted_data['country']}")
    with col2:
        if formatted_data['degree_type'] != 'Bachelors':
            st.write("Bachelors:", formatted_data['bachelors'])
        st.metric("Marks 12th:", formatted_data['marks_12th'])
        st.metric("Marks 10th:", formatted_data['marks_10th'])

        number_of_values , value = fetch_keys_values(formatted_data)
        for key,value in value.items():
            st.metric(key,value)

    result = selectbox("Select an option to start conversation",
                       [f"Top 3 universities for {formatted_data['country']}",
                        "Mock Interview", "Explain Visa Process","Mock Interview"
                        ]
                       )
    st.write("Result:", result)
    st.session_state.result = None
    if result is not None:
        st.session_state['result'] = result
        number_of_values , value = fetch_keys_values(formatted_data)
        for key,value in value.items():
            query = f'''Hi there! I am {formatted_data['username']}, I am looking to study in {formatted_data['country']},
            my {key} marks is {value},
            I want to do {formatted_data['degree_type']} in {formatted_data['field']}.
            Can you provide me with {result} of each country according to my qualifications?
            Please provide a personalized response based on my qualifications.
            Let's think step by step.'''

        st.session_state['query'] = query

        if st.button('Start Conversation'):
            switch_page('CourseBot')


    # Convert Decimal to float for better formatting


