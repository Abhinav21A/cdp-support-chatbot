# 🧑‍💻 CDP Support Chatbot

This is a **Support Agent Chatbot** that answers "how-to" questions related to four major **Customer Data Platforms (CDPs)**: 

- 📊 **Segment**
- 📈 **mParticle**
- 📋 **Lytics**
- 🔍 **Zeotap**

The chatbot dynamically scrapes the official documentation of each CDP and provides relevant answers to user queries using **fuzzy search**.

## 🚀 Features

✅ Supports four CDPs (Segment, mParticle, Lytics, Zeotap)  
✅ Dynamic web scraping using **Selenium**  
✅ Fuzzy matching for accurate search results  
✅ Mimics human-like browsing to bypass bot detection  
✅ Returns **top-3** most relevant answers  

## 📚 How It Works

1. Accepts a question via the **/chat** endpoint (POST request).
2. Identifies the correct CDP by analyzing the question.
3. Scrapes the relevant documentation using **Selenium**.
4. Uses **RapidFuzz** to find the top-3 matching answers.
5. Returns the results in a clean, numbered format.

## 🛠️ Installation

1. Clone the repository:

```bash
    git clone <your-repo-url>
    cd cdp-support-chatbot
```

2. Create a virtual environment and activate it:

```bash
# Windows
python -m venv env
.env\Scripts\activate

# Linux/macOS
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Usage

1. Start the chatbot:

```bash
python app.py
```

2. Send a **POST** request to `/chat` using **Postman** or **cURL**:

Example (for Segment):

```bash
curl -X POST "http://localhost:5000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "How do I integrate Segment?"}'
```

## 📊 Example Responses

### Request (mParticle):

```json
{
  "question": "How do I create a user profile in mParticle?"
}
```

### Response:

```json
{
  "answer": [
    "1. Navigate to the mParticle dashboard and access user profiles.",
    "2. Use the Profile API to create new user records.",
    "3. Verify integration by checking the user profile logs."
  ]
}
```

## 📦 Dependencies

- Python 3.10+
- Flask
- Selenium
- RapidFuzz
- Webdriver-Manager

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

Made with ❤️ by Abhinav Anand.
