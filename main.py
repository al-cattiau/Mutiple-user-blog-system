#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
from google.appengine.ext import db
import hashlib


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class User(db.Model):
    """ Data Model for blog User, has 2 properties,
    Article Model reference to it.
    """
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

class Article(db.Model):
    """ Data Model for blog Article, has 6 properties.
    Comment Model reference to it.
    """
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
    body = db.TextProperty(required=True)
    votes = db.StringListProperty(required=True)
    post_time = db.DateTimeProperty(auto_now_add=True)

class Comment(db.Model):
    """ Data Model for blog Comment, has 4 properties.abs
    have two reference to user who create this comment and what article commented.
    """
    user = db.ReferenceProperty(User)
    article = db.ReferenceProperty(Article)
    content = db.StringProperty(required=True)
    post_time = db.DateTimeProperty(auto_now_add=True)



# request handler class
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



class ViewHandler(MainHandler):
    """
    handle article view and main page request.
    """
    def get(self):
        """
        check the user identify, if already login, user can
        edit their article, but only can comment and like
        others article.
        """
        user = self.check_user()
        articles = self.get_all_articles()
        comments = self.get_all_comments()
        if user:
            self.render('view.html', articles=articles, user=user, comments=comments)
        else:
            self.render('view.html', articles=articles, comments=comments)

class SingleDeleteHandler(MainHandler):
    """
    handle delete single article request.
    """
    def get(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, delete the article.
        """
        user = self.check_user()
        if not user:
            return self.redirect('/view')
        article = db.get(article_key)
        if article.author.key() == user.key():
            db.delete(article_key)
        return self.redirect('/')


class VoteHandler(MainHandler):
    """
    handle article vote request.
    """
    def get(self, article_key):
        """
        check if the user already login and if article_key valid,
        if both are true, vote the article and update.
        """
        user = self.check_user()
        if not user:
            return self.redirect('/login')
        article = db.get(article_key)
        if user and article and not user.name in article.votes:
            article.votes.append(user.name)
            article.put()
        return self.redirect('/')

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


class CommentDeleteHandler(MainHandler):
    """
    handle comment delete request.
    """
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
        comment = db.get(comment_key)
        content = self.request.get('comment')
        if user and content and comment.user.key() == user.key():
            comment.content = content
            comment.put()
        return self.redirect('/')

class SignupHandler(MainHandler):
    """
    handle singup request.
    """
    def get(self):
        """
        render and response the signup web page.
        """
        self.render("signup.html")

    def post(self):
        """
        get the user name and password, add to the datastore,
        set the cookie which is the user_id.
        """
        password = self.request.get('password')
        name = self.request.get('name')
        confirm = self.request.get('confirm')

        if password and name and password == confirm:
            user = User(password=password, name=name)
            user_key = user.put()
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key', user_key)
            )
            return self.redirect('/')
        else:
            return self.render("signup.html")

class LoginHandler(MainHandler):
    """
    handle login request.
    """
    def get(self):
        """
        render the login web page.
        """
        self.render("login.html")

    def post(self):
        """
        check the password and name, if it match a User
        in the datastore, set the cookie to browser which
        is the user_key
        """
        password = self.request.get('password')
        name = self.request.get('name')
        key = self.get_user_key(name, password)
        params = dict()

        if not key:
            params['error'] = "no this user or password error"
            self.render("/login.html", **params)
        else:
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key', key)
            )
            return self.redirect('/')


class LogoutHandler(MainHandler):
    """
    handle logout request.
    """
    def get(self):
        """
        delete the user identify cookie.
        """
        self.response.delete_cookie('key')
        return self.redirect('/')

app = webapp2.WSGIApplication([
    ('/submit', SubmitHandler),
    ('/view', ViewHandler),
    ('/', ViewHandler),
    ('/signup', SignupHandler),
    ('/logout', LogoutHandler),
    ('/login', LoginHandler),
    ('/delete/(.*)', SingleDeleteHandler),
    ('/edit/(.*)', EditHandler),
    ('/vote/(.*)', VoteHandler),
    ('/comments/(.*)/', CommentHandler),
    ('/comment/delete/(.*)/', CommentDeleteHandler),
    ('/comment/edit/(.*)/', CommentEditHandler),
], debug=True)
