import langchain
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI

langchain.verbose = True

load_dotenv()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
tools = load_tools(["terminal"])
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

st.title("ChatGPT-like clone")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
