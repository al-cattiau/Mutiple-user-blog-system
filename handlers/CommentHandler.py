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



class CommentHandler(MainHandler):
    """
    handle article comment request.
    """
    def post(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, comment the article and update.
        """
        article = db.get(article_key)
        user = self.check_user()
        if not user:
            return self.redirect('/login')
        comment = self.request.get('comment')
        if user and article:
            comment = Comment(user=user, article=article, content=comment)
            comment.put()
        return self.redirect('/')


