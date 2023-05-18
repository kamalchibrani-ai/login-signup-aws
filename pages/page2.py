import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv('.env')
st.title("Page 2")
from utils import logout_button_sidebar, switch_page_if_auth_isFalse

switch_page_if_auth_isFalse()

logout_button_sidebar()

# ----------------sneha code below this------------------------------------------------


def main():



    # st.set_page_config(page_title="Ask your CSV 📈")
    st.header("Ask your CSV 📈")

    user_csv=st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        user_question=st.text_input("Ask your question about the csv: ")

        llm = OpenAI(temperature=0)
        agent=create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question != "":
            response=agent.run(user_question)
            st.write(response)



main()