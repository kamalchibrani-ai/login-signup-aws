import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if st.session_state['authenticated'] == False:
    switch_page('app')

with st.sidebar:
    if st.button('logout'):
        st.session_state['authenticated'] = False
        switch_page('app')

