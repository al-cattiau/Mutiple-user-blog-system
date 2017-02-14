from google.appengine.ext import db
from user import User


class Article(db.Model):
    """ Data Model for blog Article, has 6 properties.
    Comment Model reference to it.
    """
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
    body = db.TextProperty(required=True)
    votes = db.StringListProperty(required=True)
    post_time = db.DateTimeProperty(auto_now_add=True)

