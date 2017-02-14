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




class ViewHandler(MainHandler):
    """
    handle article view and main page request.
    """
    def get(self):
        """
        check the user identify, if already login, user can
        edit their article, but only can comment and like
        others article.
        """
        user = self.check_user()
        articles = self.get_all_articles()
        comments = self.get_all_comments()
        if user:
            self.render('view.html', articles=articles, user=user, comments=comments)
        else:
            self.render('view.html', articles=articles, comments=comments)

