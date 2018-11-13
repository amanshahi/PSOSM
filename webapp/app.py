from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_bootstrap import Bootstrap
import time, operator
from data_request import *

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '\xd4\x00;\x9a\x19y\x84\xc2yk\xd4\x1c GL\x94\xb4\xc8\x03\xdf\x94\xb4\x01|'
bootstrap = Bootstrap(app)

class ReusableForm(Form):
    facebook_name = TextField('Name:', validators=[validators.required()])

@app.route('/about')
def about():
    return 'The about page'

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    #print(form.errors)
    facebook_name = ""
    value = []
    if request.method == 'POST':
        facebook_name=request.form['facebook_name']

        if form.validate():
            flash('Hello: {}'.format(facebook_name))
        else:
            flash('Error: All Fields are Required')

    def calculate_value_based_on_username(user_given_name):
        return get_response(user_given_name)

    if facebook_name:
        value = calculate_value_based_on_username(facebook_name)
        value[3] = sorted(value[3], key=operator.itemgetter(1))[::-1]
        return render_template('index.html', form=form, value=value)
    return render_template('index.html', form=form, value=value)

if __name__ == "__main__":
    app.run()
