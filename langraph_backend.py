import getpass
import os

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


# init Model 
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


# Init Class 
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# Checkpointer 
checkpointer = InMemorySaver()

# Grap Init 
graph = StateGraph(ChatState)

# Add note 
graph.add_node('chat_node', chat_node)

# add Edege 
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compile 
chatbot = graph.compile(checkpointer=checkpointer)