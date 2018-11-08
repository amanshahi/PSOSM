from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_bootstrap import Bootstrap
import time

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '\xd4\x00;\x9a\x19y\x84\xc2yk\xd4\x1c GL\x94\xb4\xc8\x03\xdf\x94\xb4\x01|'
bootstrap = Bootstrap(app)

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route('/about')
def about():
    return 'The about page'

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    #print(form.errors)
    name = ""
    value = 0
    if request.method == 'POST':
        name=request.form['name']

        if form.validate():
            flash('Hello: {}'.format(name))
        else:
            flash('Error: All Fields are Required')

    def calculate_value_based_on_username(user_given_name):
        time.sleep(10)
        return len(name)

    if name:
        value = calculate_value_based_on_username(name)
        return render_template('index.html', form=form, value=value)
    return render_template('index.html', form=form, value=value)

if __name__ == "__main__":
    app.run()
