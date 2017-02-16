from google.appengine.ext import db
from handlers.MainHandler import MainHandler
from handlers.Decorator import _check_user_or_login
from models.article import Article


class SubmitHandler(MainHandler):
    """
    handle submit request.
    """
    def get(self):
        """
        render the article write template and response.
        """
        self.render('write.html')

    @_check_user_or_login
    def post(self):
        """
        get the user submit, fetch the article content and store in datastore.
        """
        author = self.check_user()
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n', '<br>')
        if body and title:
            article = Article(votes=[], body=body, title=title, author=author)
            article.put()
            return self.redirect('/view')
        else:
            return self.get()

