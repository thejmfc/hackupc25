# Flask backend
from flask import Flask, jsonify
from google.oauth2.service_account import Credentials
import gspread
from pymongo import MongoClient

app = Flask(__name__)

mongoDB_uri = "mongodb+srv://admin:AIR4pmONmxWtbODA@demo.j70iirs.mongodb.net/?retryWrites=true&w=majority&appName=Demo"
client = MongoClient(mongoDB_uri)

@app.route('/')
def index():
    return 'Hello there.', 200

@app.route('/process-form')
def process_form():
    return process_form(), 200



if __name__ == '__main__':
    app.run(debug=True)

