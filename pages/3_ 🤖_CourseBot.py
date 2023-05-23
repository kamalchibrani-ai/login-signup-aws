'''
1 the first query will always be from the prompt
2 next query should user input and the output should be based on previous query answer

to achieve this we need to store and pass previous query answer.

'''

import streamlit as st
from streamlit_chat import message
import openai
import os
from dotenv import load_dotenv
from utils import logout_button_sidebar

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

logout_button_sidebar()

if st.session_state.query is not None:
    prompt = [
            {
                'role': 'assistant','content': 'I am an academic consultant and i will do the following and only provide crisp information about the asked query and take content into context'
            },
            {
                "role": "user","content": f'{st.session_state.query}'
            },
    ]
    st.session_state['message_history'] = prompt

    with st.spinner('generating...'):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.5,
        )
    st.session_state.query = None

message_history = st.session_state.message_history
user_input = st.text_input('please insert a question')

if len(user_input)>0:
    message_history.append({"role": "user", "content": f"{user_input}"})
    with st.spinner('generating...'):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history,
            temperature=0.7,
        )
last_generated_content = completion.choices[0].message['content']
message_history.append({"role": "assistant", "content": f"{last_generated_content}"})

if message_history is not None:
    for i in range(len(message_history)-1, 1, -2):
        print(message_history[i])
        message(message_history[i]['content'],key=str(i))
        message(message_history[i-1]['content'],is_user=True, key=str(i-1))








