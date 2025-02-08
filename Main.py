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

# Install and import required libraries
install_and_import("googlesearch", "googlesearch-python")
install_and_import("requests")
install_and_import("bs4", "beautifulsoup4")

# Now import installed modules
import random
import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Function to fetch code snippets
def fetch_code_snippet(query):
    search_query = f"{query} site:stackoverflow.com OR site:github.com OR site:geeksforgeeks.org OR site:w3schools.com"
    
    try:
        results = search(search_query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                if any(word in soup.text.lower() for word in ["accept cookies", "subscribe", "sign-up", "cookies"]):
                    continue  

                code_blocks = soup.find_all("code")
                for code in code_blocks:
                    code_text = clean_text(code.get_text())
                    if len(code_text.split()) > 5:
                        return f"Here's a possible solution from {url}:\n\n```{code_text}```"
            except Exception:
                continue

    except Exception:
        return "I couldn't find an exact code snippet, but I can help guide you!"

    return "I searched but didn't find an exact match. Try rephrasing!"

# Function to clean up scraped text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

# Function to fetch Reddit answers
def fetch_reddit_response(query):
    search_query = f"{query} site:reddit.com"
    
    try:
        results = search(search_query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(response.text, "html.parser")

                if any(word in soup.text.lower() for word in ["accept cookies", "sign-up", "free trial", "subscribe", "log in"]):
                    continue  

                comments = soup.find_all("p")
                for comment in comments:
                    text = clean_text(comment.get_text())
                    if len(text.split()) > 10:
                        return f"Here's a Reddit response from {url}:\n\n{text}"
            except Exception:
                continue

    except Exception:
        return "I couldn't find any relevant Reddit posts."

    return "I searched Reddit but didn't find a perfect answer. Try rephrasing!"

# Function to fetch general answers from Google
def fetch_google_response(query):
    try:
        results = search(query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                if any(word in soup.text.lower() for word in ["accept cookies", "subscribe", "sign-up", "cookies"]):
                    continue  

                paragraphs = soup.find_all("p")
                for p in paragraphs:
                    text = clean_text(p.get_text())
                    if len(text.split()) > 10 and "subscribe" not in text.lower():
                        return text
            except Exception:
                continue

    except Exception:
        return "I couldn't find an exact answer, but I can help figure it out!"

    return "I searched but didn't find a perfect match. Try rephrasing!"

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
        sys.exit()
    
    if re.search(r"\b(code|example|script|program|how to)\b", user_input, re.IGNORECASE):
        return fetch_code_snippet(user_input)
    
    if "reddit" in user_input.lower():
        return fetch_reddit_response(user_input)

    return fetch_google_response(user_input)

# Main chat loop
def chat():
    print("Google AI Chatbot (Type 'exit' to quit)")
    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! Have a great day!")
            break
        response = generate_response(user_text)
        print(f"Google AI: {response}\n")

if __name__ == "__main__":
    chat()
