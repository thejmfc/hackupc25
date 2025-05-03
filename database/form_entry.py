from datetime import datetime
from mongoengine import Document, IntField, ListField, StringField


class FormEntry(Document):
    """
    Document storing data submitted by users via the form.

    Attributes:
        timestamp (str):      Datetime the request was submitted, provided by Google Forms
        group_code (str):     Unique code for the group, ties other users together in a trip
        name (str):           Name of the user
        phone_number (str):   User's phone number, used by Twilio
        airport (str):        Airport the user would like to fly from
        prefs (list):         List of freeform user preferences, contains info like desired activities, etc
        date (str):           Rough date the user would like the trip to be
        length (int):         Desired length of trip in days
    """

    DATE_FORMAT = "%-m/%w/%Y"
    TIMESTAMP_FORMAT = "%-m/%w/%Y %-H:%-M:%-S"

    # Document field definitions
    timestamp: str = StringField(required=True)
    group_code: str = StringField(required=True)
    name: str = StringField(required=True)
    phone_number: str = StringField(required=True)
    airport: str = StringField(required=True)
    prefs: list[str] = ListField(StringField(), required=True)
    date: str = StringField(required=True)
    length: int = IntField(required=True)

    @property
    def timestamp_datetime(self) -> datetime:
        return datetime.strptime(self.timestamp, FormEntry.TIMESTAMP_FORMAT)

    @property
    def date_datetime(self) -> datetime:
        return datetime.strptime(self.date, FormEntry.DATE_FORMAT)