from handlers.MainHandler import MainHandler
from handlers.Decorator import _check_comment_own, _check_article_own
from google.appengine.ext import db

class SingleDeleteHandler(MainHandler):
    """
    handle delete single article request.
    """
    @_check_article_own
    def get(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, delete the article.
        """
        db.delete(article_key)
        return self.redirect('/')


