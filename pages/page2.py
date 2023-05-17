import streamlit as st
st.title("Page 2")
from utils import logout_button_sidebar, switch_page_if_auth_isFalse

switch_page_if_auth_isFalse()

logout_button_sidebar()