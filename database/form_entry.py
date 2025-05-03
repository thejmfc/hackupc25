from datetime import datetime
from mongoengine import DateTimeField, Document, IntField, ListField, StringField


class FormEntry(Document):
    """
    Document storing data submitted by users via the form.

    Attributes:
        timestamp (datetime): Datetime the request was submitted, provided by Google Forms
        group_code (str):     Unique code for the group, ties other users together in a trip
        name (str):           Name of the user
        phone_number (str):   User's phone number, used by Twilio
        airport (str):        Airport the user would like to fly from
        prefs (list):         List of freeform user preferences, contains info like desired activities, etc
        date (datetime):      Rough date the user would like the trip to be
        length (int):         Desired length of trip in days
    """

    meta = {"collection": "forms"}

    # Document field definitions
    timestamp: datetime = DateTimeField(required=True)
    group_code: str = StringField(required=True)
    name: str = StringField(required=True)
    phone_number: str = StringField(required=True)
    airport: str = StringField(required=True)
    prefs: list[str] = ListField(StringField(), required=True)
    date: datetime = DateTimeField(required=True)
    length: int = IntField(required=True)