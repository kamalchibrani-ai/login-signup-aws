import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key, Attr
from streamlit_extras.switch_page_button import switch_page
from password_hasher import generate_hashed_pass , verify_hashed_pass
from validate import validate_username , validate_email
from database import get_resourse,get_table
import time as T
dynamodb = get_resourse()
table = get_table('users',dynamodb)


def is_valid_username(username):
    response = table.scan(FilterExpression=Attr('username').eq(username))
    return len(response['Items']) == 0
def signup():
    # st.session_state['authenticated'] = False
    username = st.text_input("Username",key='signup_username')
    password = st.text_input("Password", type="password",key='signup_password')
    email = st.text_input("Email",key='signup_email')
    if st.button("Sign up"):
        if not username or not password or not email:
            st.warning('Please fill all the fields.')
            return
        if ' ' in username:
            st.warning('Username must not contain any spaces.')
            return
        if not validate_username(username):
            st.warning('Username must contain only alphanumeric characters or underscores.')
            return
        if not validate_email(email):
            st.warning('Invalid email address.')
            return
        if not is_valid_username(username):
            st.warning('Username already exists.')
            return
        hashed_pass = generate_hashed_pass(password)
        print(hashed_pass , password)
        response = table.put_item(Item={'username': username,
                                        'password': hashed_pass,
                                        'email': email})
        if response:
            st.success('Successfully signed up! Please login.')
            st.experimental_rerun()



def login():
    username = st.text_input("Username",key='login_username')
    password = st.text_input("Password", type="password",key='login_password')

    if st.button("Login"):
        if not username or not password:
            st.warning('Please fill all the fields.')
            return
        response = table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        items = response['Items']
        print(items[0]['password'])
        print(password)
        if items:
            if verify_hashed_pass(items[0]['password'],password):
                st.success("You have successfully logged in.")
                st.session_state['username'] = username
                st.session_state['authenticated'] = True
                st.balloons()
                T.sleep(1.5)
                st.progress(1)
                table_profile = get_table('user_profile',dynamodb)
                print(table_profile)
                response_profile = table_profile.query(
                    KeyConditionExpression=Key('username').eq(username)
                )
                print(len(response_profile['Items']))
                if len(response_profile['Items'])>0:
                    st.session_state['user_profile'] = False
                    switch_page('page1')
                else:
                    st.session_state['user_profile'] = True
                    switch_page('user_profile')


            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

def logout():
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None



def main():
    # st.title("Login/Sign up App")
    st.header('Login / Sign Up')
    tab1 , tab2 = st.tabs(['Login', 'Sign up'])
    with tab1:
        login()
    with tab2:
        signup()

if __name__ == '__main__':
    main()



