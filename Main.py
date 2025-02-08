import os
import sys

# Uninstall googlesearch library if already installed
os.system(f"{sys.executable} -m pip uninstall -y googlesearch-python")

# Function to install a module if missing
def install_and_import(module_name, package_name=None):
    package_name = package_name if package_name else module_name
    try:
        __import__(module_name)
    except ImportError:
        os.system(f"{sys.executable} -m pip install --upgrade {package_name}")
        __import__(module_name)

# Install required dependencies
install_and_import("requests")
install_and_import("bs4", "beautifulsoup4")

# Now import installed modules
import random
import re
import requests
from bs4 import BeautifulSoup

# Function to fetch code snippets
def fetch_code_snippet(query):
    search_query = f"{query} site:stackoverflow.com OR site:github.com OR site:geeksforgeeks.org OR site:w3schools.com"
    print(f"Searching for: {search_query}")

    try:
        results = []  # Replace with actual search implementation if needed
        for url in results:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                # Skip cookie banners
                if any(word in soup.text.lower() for word in ["accept cookies", "subscribe", "sign-up", "free trial"]):
                    continue  

                # Extract code snippets
                code_blocks = soup.find_all("code")
                for code in code_blocks:
                    code_text = clean_text(code.get_text())
                    if len(code_text.split()) > 5:
                        return f"Here's a possible solution from {url}:\n\n{code_text}"
            except Exception:
                continue

    except Exception:
        return "I couldn't find an exact code snippet, but I can help guide you!"

    return "I searched but didn't find an exact match. Try rephrasing!"

# Function to clean up scraped text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"\[.*?\]", "", text)  # Remove citation references like [1], [2]
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
        print("Goodbye! Have a great day!")
        sys.exit(0)
    
    # Check for coding-related questions
    if re.search(r"\b(code|example|script|program|how to)\b", user_input, re.IGNORECASE):
        return fetch_code_snippet(user_input)

    return "I couldn't find an exact answer, but I can help figure it out!"

# Main chat loop
def chat():
    print("Google AI Chatbot - Type 'exit' to quit.\n")
    while True:
        user_text = input("You: ").strip()
        if user_text == "":
            continue
        response = generate_response(user_text)
        print(f"Google AI: {response}\n")

# Start chatbot
if __name__ == "__main__":
    chat()
