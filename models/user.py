from google.appengine.ext import db

class User(db.Model):
    """ Data Model for blog User, has 2 properties,
    Article Model reference to it.
    """
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)