# import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, request, render_template
import openai
import time
import numpy as np
import requests
import json

app = Flask(__name__)

file_description = open("C:/Users/DELLL/OneDrive/Máy tính/ChatGPT/chatbot_description.txt", "r+")
description = file_description.read()
history = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods = ["GET"])
def get_bot_response():
    user_message = request.args.get('msg')
    global history
    history += "\nUser: " + user_message
    prompt = description + "\n" + history + "\Brend: "

    api_key = ""
    model = "text-davinci-003"
    response = generate_response_gpt3(prompt, model, api_key)
    history += response
    return response

def generate_response_gpt3(user_message, model, api_key):
    prompt = (f"User: {user_message}\n"
              f"Brend: ")
    response = requests.post(
        "https://api.openai.com/v1/engines/text-davinci-003/completions",
        headers = {"Authorization" : f"Bearer {api_key}"},
        json={
            "prompt" : prompt,
            "max_tokens" : 1000,
            "temperature": 0.7
        },
    )

    return response.json()["choices"][0]["text"].strip()


if __name__ == "__main__":
    app.run()