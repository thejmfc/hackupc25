import database, gspread

from dotenv import load_dotenv
from flask import Flask, jsonify
from google.oauth2.service_account import Credentials

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello there.', 200

@app.route('/process-form')
def process_form():
    return process_form(), 200


if __name__ == '__main__':
    app.run(debug=True)

