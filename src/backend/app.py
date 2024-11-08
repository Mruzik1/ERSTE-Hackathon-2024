from flask import Flask, render_template, request, stream_with_context, Response, redirect, url_for, session, jsonify
from flask_cors import CORS
from model import get_response_stream
import json

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    @stream_with_context
    def generate_response():
        prompt = request.form['prompt']
        for response_chunk in get_response_stream(prompt):
            yield response_chunk
    return Response(generate_response(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)