from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment
from MainHandler import MainHandler
from Decorator import _check_user_or_login

class VoteHandler(MainHandler):
    """
    handle article vote request.
    """
    @_check_user_or_login
    def get(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, vote the article and update.
        """
        user = self.check_user()
        article = db.get(article_key)
        if user and article and not user.name in article.votes:
            article.votes.append(user.name)
            article.put()
        return self.redirect('/')

