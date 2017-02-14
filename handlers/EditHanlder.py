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


class EditHandler(MainHandler):
    """
    handle article edit request.
    """
    def get(self, article_key):
        """
        render the article write template and response.
        """
        article = db.get(article_key)
        article.body = article.body.replace('<br>', '\n')
        self.render('rewrite.html', article=article)

    def post(self, article_key):
        """
        get the user submit, fetch the article content and update in datastore.
        """
        own = self.user_own_article(article_key)
        if not own:
            self.redirect('/view')
        user = self.check_user()
        if not user:
            return self.redirect('/login')
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n', '<br>')
        article = db.get(article_key)
        if body and title and article.author.key() == user.key():
            article.title = title
            article.body = body
            article.put()
            return self.redirect('/view')
        else:
            return self.get(article_key)



