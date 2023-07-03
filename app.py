import openai
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import VectorStoreInfo, VectorStoreToolkit
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.vectorstores import Chroma

from create_index import CHROMA_PERSIST_DIRECTORY

openai.log = "debug"

load_dotenv()


def create_agent():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)

    # Setup VectorStore
    embeddings = OpenAIEmbeddings()
    db = Chroma(
        embedding_function=embeddings, persist_directory=CHROMA_PERSIST_DIRECTORY
    )
    vectorstore_info = VectorStoreInfo(
        vectorstore=db,
        name="langchain-streamlit-example",
        description="Source code of application named `langchain-streamlit-example`",
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    tools = toolkit.get_tools()

    # Setup Memory
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )


if "agent" not in st.session_state:
    st.session_state.agent = create_agent()

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
        response = st.session_state.agent.run(prompt, callbacks=[st_callback])
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
