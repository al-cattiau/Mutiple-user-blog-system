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


class LogoutHandler(MainHandler):
    """
    handle logout request.
    """
    def get(self):
        """
        delete the user identify cookie.
        """
        self.response.delete_cookie('key')
        return self.redirect('/')

