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

class SignupHandler(MainHandler):
    """
    handle singup request.
    """
    def get(self):
        """
        render and response the signup web page.
        """
        self.render("signup.html")

    def post(self):
        """
        get the user name and password, add to the datastore,
        set the cookie which is the user_id.
        """
        password = self.request.get('password')
        name = self.request.get('name')
        confirm = self.request.get('confirm')

        if password and name and password == confirm:
            user = User(password=password, name=name)
            user_key = user.put()
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key', user_key)
            )
            return self.redirect('/')
        else:
            return self.render("signup.html")

