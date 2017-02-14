import webapp2
import jinja2
import os
from google.appengine.ext import db
from models.user import User
from models.article import Article
from models.comment import Comment

template_dir = os.path.join(os.path.dirname('Mutiple-user-blog-system'), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    """ MainHandler for web system, define some basic method."""
    def write(self, *a, **kw):
        """
        write some string to response.
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
        render the html model.
        """
        template = jinja_env.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        """
        render the html model.
        """
        self.write(self.render_str(template, **kw))

    # Check the cookie
    def check_key(self):
        """
        check the user cookie for identify.
        """
        key = self.request.cookies.get('key')
        return key

    def check_user(self):
        """
        check the user identify is in the datastore or not.
        """
        key = self.check_key()
        if key:
            user = db.get(key)
            if user:
                return user

    def get_all_users(self):
        """
        get all user in the datastore
        """
        users = db.GqlQuery("SELECT * FROM User")
        return users

    def get_all_articles(self):
        """
        get all articles in the datastore
        """
        articles = db.GqlQuery("SELECT * FROM Article")
        return articles

    def get_user_key(self, name, password):
        """
        get the user key by name and password.
        """
        query = User.gql("WHERE name=:name and password=:password", name=name, password=password)
        user_query = query.get()
        if user_query:
            user_key = user_query.key()
            return user_key


    def get_all_comments(self):
        """
        get all comments in the datastore.
        """
        comments = db.GqlQuery("SELECT * FROM Comment")
        return comments

