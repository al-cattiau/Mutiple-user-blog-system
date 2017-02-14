from google.appengine.ext import db
from user import User
from article import Article


class Comment(db.Model):
    """ Data Model for blog Comment, has 4 properties.abs
    have two reference to user who create this comment and what article commented.
    """
    user = db.ReferenceProperty(User)
    article = db.ReferenceProperty(Article)
    content = db.StringProperty(required=True)
    post_time = db.DateTimeProperty(auto_now_add=True)
