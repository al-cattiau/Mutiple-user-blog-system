import webapp2
import jinja2
import os
from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment
from MainHandler import MainHandler
from Decorator import _check_article_own

class EditHandler(MainHandler):
    """
    handle article edit request.
    """
    @_check_article_own
    def get(self, article_key):
        """
        render the article write template and response.
        """
        article = db.get(article_key)
        article.body = article.body.replace('<br>', '\n')
        self.render('rewrite.html', article=article)

    @_check_article_own
    def post(self, article_key):
        """
        get the user submit, fetch the article content and update in datastore.
        """
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n', '<br>')
        article = db.get(article_key)
        if body and title:
            article.title = title
            article.body = body
            article.put()
            return self.redirect('/view')
        else:
            return self.get(article_key)



