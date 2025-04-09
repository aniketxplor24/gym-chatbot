import streamlit as st
from agent.query_handler import query_gym_data

# App configuration
st.set_page_config(page_title="Gym Assistant", page_icon="🤖", layout="centered")

col1, col2 = st.columns([1, 6])

with col1:
    st.image("data/AI bot.gif", width=60)  # Adjust path and size as needed

with col2:
    st.markdown("<h1 style='margin-top: 15px;'>Gym Manager Assistant</h1>", unsafe_allow_html=True)

st.markdown("Ask anything about your gym members, payments, or cancellations!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous conversation
for user_msg, assistant_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(assistant_msg)

# User input
user_input = st.chat_input("💬 Ask your question:")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        response = query_gym_data(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)

    # Save chat history
    st.session_state.chat_history.append((user_input, response))

