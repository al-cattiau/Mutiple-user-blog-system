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



class LoginHandler(MainHandler):
    """
    handle login request.
    """
    def get(self):
        """
        render the login web page.
        """
        self.render("login.html")

    def post(self):
        """
        check the password and name, if it match a User
        in the datastore, set the cookie to browser which
        is the user_key
        """
        password = self.request.get('password')
        name = self.request.get('name')
        key = self.get_user_key(name, password)
        params = dict()

        if not key:
            params['error'] = "no this user or password error"
            self.render("/login.html", **params)
        else:
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key', key)
            )
            return self.redirect('/')


