#!/usr/bin/env python

import wsgiref.handlers

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import facebook

api_key = "API_KEY"
secret_key = 'SECRET_KEY'
session_key = 'YOUR_SESSION_KEY'

class Main(webapp.RequestHandler):
    def get(self, action = ""):       
        # Check to see if logged        
        fb = facebook.Facebook(api_key, secret_key)        
        validSession = fb.check_session(self.request)           
        session_key = fb.session_key
        
        if validSession == True:
            self.response.out.write("<fb:redirect url=\"http://apps.facebook.com/knowyourprivacy/\" />")
        else:
            self.response.out.write("<fb:redirect url=\"http://apps.facebook.com/knowyourprivacy/\" />")
    
    def post(self, action = ""):
        fb = facebook.Facebook(api_key, secret_key)        
        validSession = fb.check_session(self.request)
        
        if validSession == True:    
            #Open the template.
            path = os.path.join(os.path.dirname(__file__), "facebookTemplate.html")
            info = fb.users.getInfo([fb.uid], ['name', 'first_name', 'pic', 'last_name' ,'birthday', 'affiliations', 'movies', 'music', 'tv', 'sex', 'education_history', 'work_history', 'hs_info', 'interests', 'hometown_location', 'current_location', 'about_me'])[0]
            friends = fb.friends.get()
            friends = fb.users.getInfo(friends[0:10], ['name', 'first_name', 'pic', 'last_name' ,'birthday', 'affiliations', 'movies', 'music', 'tv', 'sex', 'education_history', 'work_history', 'hs_info', 'interests', 'hometown_location', 'current_location', 'about_me'])
            self.response.out.write(template.render(path, {"uid": fb.uid, "info":info, "friends": friends}))
        else:
            self.response.out.write("Many facebook applications need authorisation to be able to access your account, normally you will simply accept the request without thinking twice about it. To be able to show you the data that is visible to these applications Know Your Privacy requires you to authorise the application.  <a href=\"http://apps.facebook.com/knowyourprivacy\" requirelogin=1>Authorise Know Your Privacy Now!</a>." )
        
def main():
    application = webapp.WSGIApplication([(r'/facebook/auth', Main), (r'/facebook/auth/',Main)])
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == "__main__":
    main()