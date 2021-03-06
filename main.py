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

class Message(ndb.Model):
    sender_name = ndb.StringProperty()
    email_address = ndb.StringProperty()
    message = ndb.StringProperty()

class AboutApp(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about_us.html')
        self.response.out.write(template.render())

class FeedbackHandler(webapp2.RequestHandler):
    def get(self):
        sender_name = ""
        email_address = ""
        message = ""
        query = Message.query() #query queries the database for messages
        message_list = query.fetch() #fetch fetches the list of messages from the database and puts it into a variable
        i=0
        for n in message_list:
            i+=1
        template = jinja_environment.get_template('feedback.html')
        variables = {
            'message': message,
            'sender_name': sender_name,
            'email_address': email_address,
            'message_list': message_list,
            'i': i}
        self.response.out.write(template.render(variables))

    def post(self):
        message_key = ndb.Key('Message', self.request.get('sender_name'))
        message = message_key.get()

        if not message:
            message = Message(
                sender_name = self.request.get('sender_name'),
                email_address =  self.request.get('email_address'),
                message =  self.request.get('message'))
        message.key = message_key
        message.put()
        self.redirect('/feedback')


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
        template = jinja_environment.get_template('login.html')
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
        weather = content_dict['weather'][0]['description']
        my_vars= {
        'zip_code': zip_code,
        'city': city,
        'temp': temp,
        'weather': weather
        }

        template = jinja_environment.get_template('chooseoutfit.html')
        self.response.out.write(template.render(my_vars))


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
    ('/feedback', FeedbackHandler),
    ('/login', LoginHandler),
    ('/', HomePageHandler),
    ('/choose_outfit', ChooseOutfitHandler),
    ('/styles_colors', StylesColorsHandler)
], debug=True)
