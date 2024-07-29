import os
from flask import Flask, render_template
import google.generativeai as genai
import re

app = Flask(__name__)

# Configure the API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

def extract_json(text):
    # Find the content between the first { and the last }
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None

@app.route('/get_capitals')
def get_capitals():
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Please return your response as the form of JSON with ten key value pairs of Asian countries and their capitals"
    response = model.generate_content(prompt)
    cleaned_response = extract_json(response.text.strip())

    return cleaned_response  # Return the cleaned text response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)