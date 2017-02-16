from handlers.Decorator import _check_user_or_login
from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment
from MainHandler import MainHandler

class CommentDeleteHandler(MainHandler):
    """
    handle comment delete request.
    """
    @_check_user_or_login
    def get(self, comment_key):
        """
        check if the user already login and if comment_key valid,
        if both are true, delete the comment.
        """
        user = self.check_user()
        comment = db.get(comment_key)
        if comment.user.key() == user.key() and user:
            db.delete(comment_key)
        return self.redirect('/')

