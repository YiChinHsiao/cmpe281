from flask import Flask, render_template
from application import db
from application.models import *
import os

application = Flask(__name__)

db.create_all()

@application.route('/')
@application.route('/homepage')
def homepage():
    data = User.query.filter_by(user_id='Gary').first()
    email = data.email 
    return render_template('homepage.html', email=email)
    

if __name__ == '__main__':
    application.run(debug = True)

