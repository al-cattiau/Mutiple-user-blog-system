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




class CommentEditHandler(MainHandler):
    """
    handle comment edit request.
    """
    def post(self, comment_key):
        """
        check if the user already login and if comment_key valid,
        if both are true, edit and update the comment.
        """
        user = self.check_user()
        comment = Comment.get_by_id(comment_key)
        content = self.request.get('comment')
        if user and content and comment.user.key() == user.key():
            comment.content = content
            comment.put()
        return self.redirect('/')

