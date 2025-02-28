from flask import Flask, request, jsonify
from rapidfuzz import process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return "CDP Support Chatbot is Running!"

# Helper function to scrape content from a given URL
def scrape_content(url):
    try:
        # Randomize user agents to mimic human behavior
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set random user-agent
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        # Manage ChromeDriver automatically
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get(url)

        # Mimic user scrolling behavior
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        # Capture visible content
        elements = driver.find_elements(By.XPATH, "//*[not(self::script or self::style)]")
        content = [element.text for element in elements if element.text.strip()]

        # Debug: Print first 20 lines
        print(f"Scraped content from {url}:", content[:20])

        driver.quit()
        return content

    except Exception as e:
        return [f"Error while scraping {url}: {e}"]

# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('question')
    if not user_query:
        return jsonify({"error": "Please provide a question."}), 400

    # Identify which CDP to scrape based on the query
    cdp_sources = {
        "segment": "https://segment.com/docs/",
        "mparticle": "https://docs.mparticle.com/",
        "lytics": "https://docs.lytics.com/",
        "zeotap": "https://docs.zeotap.com/home/en-us/"
    }

    # Determine the source based on the query
    matched_source = None
    for cdp, url in cdp_sources.items():
        if cdp in user_query.lower():
            matched_source = url
            break

    if not matched_source:
        return jsonify({"error": "Please specify a valid CDP (Segment, mParticle, Lytics, Zeotap)."}), 400

    # Fetch and search content
    content = scrape_content(matched_source)

    # Perform fuzzy search (top 3 matches)
    results = process.extract(user_query, content, limit=3)

    # Remove duplicates and format the response
    unique_results = list(dict.fromkeys([result[0] for result in results]))

    formatted_results = [f"{i + 1}. {item[:500]}" for i, item in enumerate(unique_results)]

    return jsonify({"answer": formatted_results})

if __name__ == '__main__':
    app.run(debug=True)




