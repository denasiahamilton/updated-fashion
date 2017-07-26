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

class AboutApp(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about_us.html')
        self.response.out.write(template.render())

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
        zip_code = self.request.get('zip_code')
        if not zip_code:
            zip_code = 98103
        api_url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + str(zip_code) + '&APPID=63b5494aec29fe7add0c7d0975dd7feb'
        logging.info(api_url)
        response = urllib2.urlopen(api_url)
        content = response.read()
        content_dict = json.loads(content)
        city = content_dict['name']
        temp = content_dict['main']['temp']
        temp = int(round(1.8 * (temp - 273) + 32))
        my_vars= {
        'zip_code': zip_code,
        'city': city,
        'temp': temp
        }

        template = jinja_environment.get_template('chooseoutfit.html')
        self.response.out.write(template.render(my_vars))

class CityHandler(webapp2.RequestHandler):
    def post(self):
        pass


class StylesColorsHandler(webapp2.RequestHandler):
    def get(self):
        """color = self.request.get('color')
        if not color:
            color = "00ffa6"
        api_url = 'http://www.thecolorapi.com/form-id?hex=' + color
        response = urllib2.urlopen(api_url)
        content = response.read()
        content_dict = json.loads(content)
        #what is content_dict? a list? of strings? color hex number? color name?
        value = content_dict['value']"""
        template = jinja_environment.get_template('style_and_color.html')
        """my_vars = {
            'color': color,
            'content': content,
            "value": value
        }"""
        self.response.out.write(template.render())



app = webapp2.WSGIApplication([
    ('/about_us', AboutApp),
    ('/login', LoginHandler),
    ('/', HomePageHandler),
    ('/choose_outfit', ChooseOutfitHandler),
    ('/styles_colors', StylesColorsHandler)

], debug=True)
