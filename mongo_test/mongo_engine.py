from mongoengine import *

db = connect('test', host='localhost', port=27017)


class User2(Document):
    name = StringField(required=True, max_length=64)
    age = IntField(required=True)


class Paper(Document):
    content = StringField(required=True, max_length=256)
    user = ReferenceField(User2)
