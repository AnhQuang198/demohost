from mongoengine import *

class fooditem(Document):
    src = StringField()
    image = FileField()
    title = StringField()
    description = StringField()