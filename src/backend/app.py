import os
from flask import Flask, render_template, request, stream_with_context, Response, redirect, url_for, session, jsonify
from flask_cors import CORS
from model import get_response_stream
from tools import infer_llm
import json

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    response = infer_llm(prompt)
    return jsonify({'response': f"<img src=\"{response}\" alt=\"Plot\" style=\"width: 600px; border-radius: 10%; overflow: hidden;\">" if "../" in response else response})

if __name__ == '__main__':
    app.run(host="localhost", port=5000)