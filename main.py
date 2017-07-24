import logging
import os
import jinja2
import json
import urllib
import urllib2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(
    loader= jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates')
        )

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        cur_user = users.get_current_user()
        logging.info(str(cur_user))
        log_url = ''
        if cur_user:
            log_url = users.create_logout_url('/login')
        else:
            log_url = users.create_login_url('/')
            logging.info(log_url)
        template = jinja_environment.get_template('main.html')
        var = {
            'user' :cur_user,
            'log_url': log_url
        }
        self.response.out.write(template.render(var))

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
            cur_user = users.get_current_user()
            log_url = ''
            if cur_user:
                log_url = users.create_logout_url('/')
            else:
                log_url = users.create_login_url('/')
            template = jinja_environment.get_template('homepage.html')
            var = {
                'user' :cur_user,
                'log_url': log_url
            }
            template = jinja_environment.get_template('homepage.html')
            self.response.out.write(template.render(var))

class ChooseOutfitHandler(webapp2.RequestHandler):
    def get(self):
        zip_code = 98103
        if not zip_code:
            zip_code = 98103
        api_url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + str(zip_code) + '&APPID=63b5494aec29fe7add0c7d0975dd7feb'
        logging.info(api_url)
        response = urllib2.urlopen(api_url)
        content = response.read()
        content_dict = json.loads(content)
        my_vars= {'q':zip_code}
        template = jinja_environment.get_template('chooseoutfit.html')
        self.response.out.write(template.render(my_vars))

class CityHandler(webapp2.RequestHandler):
    def post(self):
        pass


class StylesColorsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/', HomePageHandler),
    ('/choose_outfit', ChooseOutfitHandler),
    ('/styles_colors', StylesColorsHandler)

], debug=True)
