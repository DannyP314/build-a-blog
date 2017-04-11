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
import cgi
import jinja2
import os
from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post")
        t = jinja_env.get_template("new_post.html")
        content = t.render(posts=posts)
        self.response.write(content)

    def post(self):
        title = self.request.get("title")
        newpost = self.request.get("newpost")
        error = ""
        t = jinja_env.get_template("new_post.html")
        content = t.render(title = title, newpost = newpost, error = error)
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        if title and newpost:
            p = Post(title = title, post = newpost)
            p.put()

            self.redirect("/")
        else:
            error="Submissions require a Title and text to post!"

        content = t.render(title = title, newpost = newpost, error = error, posts = posts)
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
