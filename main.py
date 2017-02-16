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


from handlers.CommentDeleteHandler import CommentDeleteHandler
from handlers.CommentEditHandler import CommentEditHandler
from handlers.EditHanlder import EditHandler
from handlers.LogoutHandler import LogoutHandler
from handlers.SignupHanlder import SignupHandler
from handlers.SingleDeleteHandler import SingleDeleteHandler
from handlers.SubmitHandler import SubmitHandler
from handlers.VoteHandler import VoteHandler
from handlers.ViewHandler import ViewHandler
from handlers.CommentHandler import CommentHandler
from handlers.LoginHanlder import LoginHandler


app = webapp2.WSGIApplication([
    ('/comment/delete/(.*)/', CommentDeleteHandler),
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
    ('/comment/edit/(.*)/', CommentEditHandler),
], debug=True)
