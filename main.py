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
import time
import os
import jinja2
from google.appengine.ext import db
import hashlib


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
secret = 'lyz'

# deta model 
class Article(db.Model):
    title = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    votes = db.StringListProperty(required=True)
    post_time = db.DateTimeProperty(auto_now_add = True)
    

class User(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)


# request handler class
class MainHandler(webapp2.RequestHandler):    
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    def checkKey(self):
        key = self.request.cookies.get('key')
        return key

    def checkUser(self):
        key = self.checkKey()
        if key:
            user = db.get(key)
            if user:
                return user

    def getAllUsers(self):
        users = db.GqlQuery("SELECT * FROM User")
        return users

    def getAllArticles(self):
        articles = db.GqlQuery("SELECT * FROM Article")
        return articles

    def getUserKey(self,name,password):
        user_query = User.gql("WHERE name=:name and password=:password",name=name,password=password).get()
        if user_query:
            user_key = user_query.key()
            return user_key



class SubmitHandler(MainHandler):
    def get(self):
        self.render('write.html')

    def post(self):
        user = self.checkUser();
        author = user.name;
        if not author:
            self.redirect('/login')            
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n','<br>')
        if body and title:
            
            article = Article(votes=[],body=body,title=title,author=author)
            
            key = article.put()

            time.sleep(0.1)
            self.redirect('/view')
        else:
            self.get()

class EditHandler(MainHandler):
    def get(self,article_key):
        article = db.get(article_key)
        article.body = article.body.replace('<br>','\n')
        self.render('rewrite.html',article=article)


    def post(self,article_key):
        author = self.checkUser();
        if not author:
            self.redirect('/login')            
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n','<br>')
        article = db.get(article_key)
        if body and title:
            article.title = title
            article.body = body
            article.put()
            time.sleep(0.1)
            self.redirect('/view')
        else:
            self.get()



class ViewHandler(MainHandler):
    def get(self):
        user = self.checkUser()
        
        articles = self.getAllArticles()
        if user:
            self.render('view.html',articles=articles,user_name=user.name)
        else:
            self.render('view.html',articles=articles,disabled="True")


class DeleteHandler(MainHandler):
    def get(self):
        articles = db.GqlQuery("SELECT * FROM Article")
        users = db.GqlQuery("SELECT * FROM User")
        for user in users:
            user.delete()
        for article in articles:
            article.delete()
        
class SingleDeleteHandler(MainHandler):
    def get(self,article_key):
        user = self.checkUser()
        article = db.get(article_key)
        if article.author == user.name :
            db.delete(article_key)

        time.sleep(0.1)
        self.redirect('/')
    
        
class VoteHandler(MainHandler):
    def get(self,article_key):
        user = self.checkUser()
        article = db.get(article_key)
        if user and article:
            article.votes.append(user.name)
            
        self.redirect('/')





class SignupHandler(MainHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        password = self.request.get('password')
        name = self.request.get('name')
        confirm = self.request.get('confirm')

        if password and name and password == confirm:
            user = User(password=password,name=name)
            user_key = user.put()
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key',user_key)
            )
            self.redirect('/')
        else:
            self.render("signup.html")

class LoginHandler(MainHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        password = self.request.get('password')
        name = self.request.get('name')
        key = self.getUserKey(name,password)
        params = dict()

        if not key:
            params['error'] = "no this user or password error"
            self.render("/login.html",**params)            
        else:
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('key',key)
            )
            self.redirect('/')
            


class LogoutHandler(MainHandler):
    def get(self):
        self.response.delete_cookie('key')
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/submit', SubmitHandler),
    ('/view',ViewHandler),
    ('/',ViewHandler),
    ('/deleteall',DeleteHandler),
    ('/signup',SignupHandler),
    ('/logout',LogoutHandler),
    ('/login',LoginHandler),
    ('/delete/(.*)',SingleDeleteHandler),
    ('/edit/(.*)',EditHandler),
    ('/vote/(.*)',VoteHandler)

], debug=True)
