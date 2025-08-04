import streamlit as st
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Config 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Session State 
if 'messages_history' not in st.session_state:
  st.session_state['messages_history'] = []

for message in st.session_state['messages_history']:
  with st.chat_message(message['role']):
    st.text(message['content'])

# User Input 
user_input = st.chat_input('Type here')

# without streammming 

# if user_input:

#   st.session_state['messages_history'].append({'role': 'user', 'content' : user_input})
#   with st.chat_message('user'):
#     st.text(user_input)
  
#   response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
#   ai_response = response['messages'][-1].content

#   st.session_state['messages_history'].append({'role': 'assistant', 'content' : ai_response})
#   with st.chat_message('assistant'):
#     st.text(ai_response)


# with Streamming 
if user_input:

  st.session_state['messages_history'].append({'role': 'user', 'content' : user_input})
  with st.chat_message('user'):
    st.text(user_input)

  with st.chat_message('assistant'):
    ai_response = st.write_stream(
      message_chunk.content for message_chunk, metadata in chatbot.stream(
        {'messages': [HumanMessage(content=user_input)]},
        config=CONFIG,
        stream_mode='messages'
      )
    )
  

  st.session_state['messages_history'].append({'role': 'assistant', 'content' : ai_response})