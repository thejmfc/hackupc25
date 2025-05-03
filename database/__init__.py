import os

from .form_entry import  *
from dotenv import load_dotenv
from mongoengine import connect


load_dotenv()

# Initialise connection to MongoDB
connect(host=os.environ["MONGODB_URI"])