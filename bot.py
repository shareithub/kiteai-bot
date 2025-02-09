import shareithub
import requests
import json
import time
import random
import os
from shareithub import shareithub
from faker import Faker
from termcolor import colored
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

fake = Faker()

agents = {
    "deployment_p5J9lz1Zxe7CYEoo0TZpRVay": "Professor",
    "deployment_7sZJSiCqCNDy9bBHTEh7dwd9": "Crypto Buddy"
}

API_KEY = os.getenv("API_KEY")
WALLETS = os.getenv("WALLETS", "").split(",")
headersFilePath = 'headers.json'
rateLimitExceeded = False
shareithub()

def display_app_title():
    print(colored('\n🚀 AI & Blockchain Automation Script 🚀', 'cyan', attrs=['bold']))
    print(colored('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'blue'))

def load_headers():
    if os.path.exists(headersFilePath):
        with open(headersFilePath, 'r') as f:
            return json.load(f)
    return {}

def save_headers(headers):
    with open(headersFilePath, 'w') as f:
        json.dump(headers, f, indent=2)

def generate_random_desktop_header():
    return {"User-Agent": fake.user_agent()}  

def get_random_theme():
    themes = [
        "Proof of Attributed Intelligence (PoAI)", "Decentralized AI Governance",
        "Democratization of AI Economy", "AI-powered Smart Contracts",
        "Blockchain-based AI Marketplaces", "Autonomous AI Agents on Blockchain",
        "Scalability Challenges in AI & Blockchain", "Zero-Knowledge Proofs for AI Privacy",
        "AI and Blockchain Synergy for Cybersecurity", "Energy Efficiency in AI Blockchain Networks"
    ]
    return random.choice(themes)

def generate_random_words():
    words = {
        "subjects": ["AI", "blockchain", "smart contracts", "scalability", "security", "privacy", "decentralization", "automation", "trust", "efficiency"],
        "verbs": ["improve", "affect", "contribute", "enhance", "drive", "change", "transform", "reduce", "optimize", "strengthen"],
        "objects": ["technology", "systems", "applications", "networks", "protocols", "platforms", "transactions", "processes", "infrastructure", "economy"],
        "questions": ["How", "What", "Can", "Why", "Does", "What is the impact of", "How does", "What effect does", "Can", "How can"],
        "modifiers": ["the future of", "the efficiency of", "the security of", "the scalability of", "the integration of", "the development of", "the adoption of"]
    }
    return f"{random.choice(words['questions'])} {random.choice(words['subjects'])} {random.choice(words['verbs'])} {random.choice(words['modifiers'])} {random.choice(words['objects'])}?"

def generate_random_question():
    global rateLimitExceeded
    theme = get_random_theme()
    if rateLimitExceeded:
        return generate_random_words()
    
    try:
        response = requests.post('https://api.groq.com/openai/v1/chat/completions',
                                 headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
                                 json={'model': 'llama-3.3-70b-versatile',
                                       'messages': [{'role': 'user', 'content': f'Generate a question about {theme} in AI and blockchain.'}],
                                       'temperature': 0.9})
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException:
        rateLimitExceeded = True
        return generate_random_words()

def process_wallet(wallet, headers, iterationsPerAgent):
    print(colored(f"\n💰 Processing Wallet: {wallet}", 'green', attrs=['bold']))
    for agent_id, agent_name in agents.items():
        print(colored(f"\n🤖 Agent: {agent_name}", 'magenta', attrs=['bold']))
        print(colored('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'blue'))
        for i in range(iterationsPerAgent):
            print(colored(f"⚡ Task-{i + 1}", 'yellow', attrs=['bold']))
            question = generate_random_question()
            print(colored("📌 Question:", 'cyan'), colored(question, attrs=['bold']))
            time.sleep(1)
        print(colored('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'blue'))

def main():
    display_app_title()
    headers = load_headers()
    iterationsPerAgent = 7

    for wallet in WALLETS:
        if wallet and wallet not in headers:
            headers[wallet] = generate_random_desktop_header()
            save_headers(headers)
        try:
            process_wallet(wallet, headers, iterationsPerAgent)
        except Exception as e:
            print(colored(f"❌ Failed to process wallet {wallet}: {e}", 'red', attrs=['bold']))

    random_time = random.randint(3 * 3600, 7 * 3600)
    print(colored(f"⏳ Waiting for {random_time} seconds before restarting...", 'yellow', attrs=['bold']))
    time.sleep(random_time)
    global rateLimitExceeded
    rateLimitExceeded = False
    main()

if __name__ == "__main__":
    main()
