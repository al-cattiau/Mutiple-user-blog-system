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


class SubmitHandler(MainHandler):
    def get(self):
        self.render('write.html')

    def post(self):
        author = self.request.cookies.get('name')
        if not author:
            self.redirect('/login')            
        title = self.request.get('title')
        body = self.request.get('body')
        body = body.replace('\n','<br>')
        if body and title:

            article = Article(body=body,title=title,author=author)
            article.put()

            time.sleep(0.1)
            self.redirect('/view')
        else:
            self.get()


class ViewHandler(MainHandler):
    def get(self):
        articles = db.GqlQuery("SELECT * FROM Article")
        #print articles[0].title
        cookie = self.request.cookies.get('name')
        if cookie:
            self.render('view.html',articles=articles,user_name=cookie)
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
        

class RegisterHandler(MainHandler):
    def get(self):
        self.render("sign.html",method='Resgiter')

    def post(self):
        password = self.request.get('password')
        name = self.request.get('name')

        if password and name:
            user = User(password=password,name=name)
            user.put()
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('name',str(name))
            )
            self.redirect('/')

class LoginHandler(MainHandler):
    def get(self):
        self.render("sign.html",method='Login')

    def post(self):
        password = self.request.get('password')
        name = self.request.get('name')

        p_password = db.GqlQuery("SELECT * FROM User WHERE name = :name",name=name).get().password        
        params = dict()

        print str(password),str(p_password)
        if not p_password:
            params['error'] = "no this user"
            self.render("/sign.html",**params)
        elif not p_password == password:
            params['error'] = "password error"
            self.render("/sign.html",**params)
        else:
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s;Path=/' %('name',str(name))
            )
            self.redirect('/')
            


class LogoutHandler(MainHandler):
    def get(self):
        self.response.delete_cookie('name')
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/submit', SubmitHandler),
    ('/view',ViewHandler),
    ('/',ViewHandler),
    ('/delete',DeleteHandler),
    ('/register',RegisterHandler),
    ('/logout',LogoutHandler),
    ('/login',LoginHandler)
], debug=True)
