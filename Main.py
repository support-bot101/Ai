import os
import sys

# Install required dependencies
os.system(f"{sys.executable} -m pip install --upgrade streamlit requests beautifulsoup4")

# Now import installed modules
import random
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Function to fetch code snippets (Dummy implementation for now)
def fetch_code_snippet(query):
    return f"Sorry, but I can't fetch live results. Try searching '{query}' on Stack Overflow or GitHub."

# Function to clean up text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"\[.*?\]", "", text)  # Remove citation references
    return text.strip()

# Function to generate responses
def generate_response(user_input):
    if re.search(r"\b(hi|hello|hey)\b", user_input, re.IGNORECASE):
        return random.choice(["Hey there!", "Hello! How can I assist you today?", "Hi! Need help with something?"])
    elif re.search(r"\b(how are you)\b", user_input, re.IGNORECASE):
        return "I'm just a chatbot, but I'm here to help! How about you?"
    elif re.search(r"\b(who are you|what is your name)\b", user_input, re.IGNORECASE):
        return "I'm Google AI, your chatbot assistant!"
    elif re.search(r"\b(exit|quit|bye)\b", user_input, re.IGNORECASE):
        return "Goodbye! Have a great day!"

    # Check for coding-related questions
    if re.search(r"\b(code|example|script|program|how to)\b", user_input, re.IGNORECASE):
        return fetch_code_snippet(user_input)

    return "I couldn't find an exact answer, but I can help figure it out!"

# Streamlit UI
st.title("Google AI Chatbot")

st.write("Ask me anything!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = "👤 You" if message["role"] == "user" else "🤖 Google AI"
    st.write(f"**{role}:** {message['content']}")

# User input
user_input = st.text_input("Type your message:", key="input")

if user_input:
    response = generate_response(user_input)

    # Save messages
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "bot", "content": response})

    # Refresh the chat UI
    st.rerun()
