import webapp2
import jinja2
import os
from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment
from MainHandler import MainHandler

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))




class SingleDeleteHandler(MainHandler):
    """
    handle delete single article request.
    """
    def get(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, delete the article.
        """
        user = self.check_user()
        if not user:
            return self.redirect('/view')
        article = db.get(article_key)
        if article.author.key() == user.key():
            db.delete(article_key)
        return self.redirect('/')


