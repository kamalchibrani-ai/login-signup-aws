import streamlit as st
from streamlit_extras.switch_page_button import switch_page





def switch_page_if_auth_isFalse():
    if st.session_state['authenticated'] == False:
        switch_page('app')

def switch_page_if_userProfile_isFalse():
    if st.session_state['user_profile'] == False:
        switch_page('Profile')

def logout_button_sidebar():
    with st.sidebar:
        if st.button('logout'):
            st.session_state['authenticated'] = False
            switch_page('app')

def things_with_sidebar(username):
    with st.sidebar:
        st.subheader('Welcome ' + username)