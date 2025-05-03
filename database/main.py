import os

from mongoengine import connect

# Initialise connection to MongoDB
connect(os.environ["MONGODB_URI"])