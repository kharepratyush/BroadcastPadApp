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
 
template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template, **params):
		t=jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))

class Data(db.Model):
	room=db.StringProperty(required=True)
	hostel=db.StringProperty(required=True)
	info=db.StringProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)

class MainHandler(Handler):
    def render_front(self,room="",hostel="",info="",error=""):
    	datum=db.GqlQuery("SELECT * FROM Data ORDER BY created ASC")
    	self.render("front.html",room="", hostel="", info="", created="", error=error, datum=datum)


    def get(self):
    	error=""
        self.render_front()

    def post(self):
        room=self.request.get('room')
        hostel=self.request.get('hostel')
        info=self.request.get('info')

        if room and hostel and info:
            #self.write("Thanx")
            d=Data(room=room, hostel=hostel,info=info)
            d.put()
            self.redirect("/")
            #self.render_front()

        else:
            self.render_front(error="Error Generated.. Enter correct values")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
