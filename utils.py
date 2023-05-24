import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import webbrowser





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
        st.button("Contact us!", on_click=open_support_ticket)


def EmailUs():
    with st.sidebar:
        st.button("Contact us!", on_click=open_support_ticket)


def open_support_ticket():
    email_link = f"mailto:kchibrani@gmail.com?bcc=snehasantosh103@gmail.com&subject=I%20am%20Interested%20in%20getting%20consultation&body=Hello%2C%20I'm%20looking%20forward%20to%20study%20abroad.%20I%20would%20like%20you%20to%20contact%20me%20back.%20%0A%0AThanks%2C%0A{st.session_state.username}"
    webbrowser.open(email_link)