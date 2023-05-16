import re
import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key, Attr

import os
from dotenv import load_dotenv
load_dotenv('.env')
YOUR_ACCESS_KEY = os.getenv('aws_access_key_id')
YOUR_SECRET_KEY = os.getenv('aws_secret_access_key')

# Function to validate email address
def is_valid_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email)

# Function to validate password
def is_valid_password(password):
    return len(password) >= 8

# Function to handle user sign up
def signup():
    # Get user input
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    
    # Validate email and password
    if not is_valid_email(email):
        st.error("Please enter a valid email address")
        return
    
    if not is_valid_password(password):
        st.error("Password must be at least 8 characters long")
        return
    
    # Add user to DynamoDB table
    table.put_item(
        Item={
            "username": username,
            "password": password,
            "email": email
        }
    )
    st.success("You have successfully signed up! Please log in.")

# Function to handle user login
def login():
    # Get user input
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Retrieve user from DynamoDB table
    response = table.query(
        KeyConditionExpression=Key("username").eq(username)
    )
    
    # Check if user exists and password is correct
    if response["Count"] == 0:
        st.error("Username not found")
        return
    
    user = response["Items"][0]
    if user["password"] != password:
        st.error("Incorrect password")
        return
    
    # Set authentication status to True and display username in sidebar
    st.sidebar.success("Logged in as {}".format(username))
    st.session_state.authenticated = True
    st.session_state.username = username

# Function to handle user logout
def logout():
    # Set authentication status to False and username to None
    st.session_state.authenticated = False
    st.session_state.username = None

# Function to handle forgot username
def forgot_username():
    # Get user input
    email = st.text_input("Email")
    
    # Retrieve user from DynamoDB table
    response = table.scan(
        FilterExpression=Attr("email").eq(email)
    )
    
    # Check if user exists and display username
    if response["Count"] > 0:
        username = response["Items"][0]["username"]
        st.success("Your username is {}".format(username))
    else:
        st.error("Email not found")

# Function to handle forgot password
def forgot_password():
    # Get user input
    username = st.text_input("Username")
    email = st.text_input("Email")
    
    # Retrieve user from DynamoDB table
    response = table.query(
        KeyConditionExpression=Key("username").eq(username)
    )
    
    # Check if user exists and send password reset email
    if response["Count"] > 0 and response["Items"][0]["email"] == email:
        # send_password_reset_email(email)
        # st.success("Password reset email sent")
        st.success("Password reset email sent")
    else:
        st.error("Username or email not found")


def main():
    # Create DynamoDB resource
    dynamodb_resource = boto3.resource("dynamodb")
    global table
    table = dynamodb_resource.Table("users")
    
    # Create Streamlit app
    st.title("Login/Sign up App")
    st.session_state.authenticated = False
    st.session_state.username = None
    
    # Create tabs
    tabs = ["Login", "Sign up", "Forgot Username", "Forgot Password"]
    selected_tab = st.sidebar.selectbox("Select an action", tabs)
    
    # Call appropriate function based on selected tab
    if selected_tab == "Login":
        login()
    elif selected_tab == "Sign up":
        signup()
    elif selected_tab == "Forgot Username":
        forgot_username()
    elif selected_tab == "Forgot Password":
        forgot_password()
    
    # Display logout button if user is authenticated
    if st.session_state.authenticated:
        st.sidebar.button("Logout", on_click=logout)