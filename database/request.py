import mongoengine


class Request(mongoengine.Document):
    timestamp = mongoengine.DateTimeField(required=True)
    group_code = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    phone_number = mongoengine.StringField(required=True)
    airport = mongoengine.StringField(required=True)
    prefs = mongoengine.ListField(mongoengine.StringField(), required=True)
    date = mongoengine.DateTimeField(required=True)
    length = mongoengine.IntField(required=True)