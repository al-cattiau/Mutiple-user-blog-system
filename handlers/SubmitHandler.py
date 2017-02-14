import webapp2
import jinja2
import os
from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment
from handlers.MainHandler import MainHandler

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class SubmitHandler(MainHandler):
    """
    handle submit request.
    """
    def get(self):
        """
        render the article write template and response.
        """
        self.render('write.html')

    def post(self):
        """
        get the user submit, fetch the article content and store in datastore.
        """
        user = self.check_user()
        if not user:
            return self.redirect('/view')
        author = user.key()
        if not author:
            return self.redirect('/login')
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n', '<br>')
        if body and title:
            article = Article(votes=[], body=body, title=title, author=author)
            article.put()
            return self.redirect('/view')
        else:
            return self.get()

