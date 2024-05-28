"""
A sample frontend server. Hosts a web page to display messages
"""
import json
import os
import datetime
import time
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm, CSRFProtect
import requests
import dateutil.relativedelta

DEFAULT_GUESTBOOK_API_ADDR = "127.0.0.1:8321"
GUESTBOOK_API_ADDR = os.environ.get('GUESTBOOK_API_ADDR', DEFAULT_GUESTBOOK_API_ADDR)
DEFAULT_PORT = 8123
PORT = os.environ.get('PORT', DEFAULT_PORT)
DEFAULT_HOST = "127.0.0.1"
HOST = os.environ.get('HOST', DEFAULT_HOST)
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["BACKEND_URI"] = f'http://{GUESTBOOK_API_ADDR}/messages'
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)

class MyForm(FlaskForm):
    pass


@app.route('/')
def main():
    form = MyForm()
    """ Retrieve a list of messages from the backend, and use them to render the HTML template """
    response = requests.get(app.config["BACKEND_URI"], timeout=3)
    json_response = json.loads(response.text)
    return render_template('home.html', form=form, messages=json_response)

@app.route('/post', methods=['POST'])
def post():
    """ Send the new message to the backend and redirect to the homepage """
    form = MyForm()
    if form.validate_on_submit():
        new_message = {'author': request.form['name'],
                    'message':  request.form['message']}
        requests.post(url=app.config["BACKEND_URI"],
                    data=jsonify(new_message).data,
                    headers={'content-type': 'application/json'},
                    timeout=3)
        return redirect(url_for('main'))

def format_duration(timestamp):
    """ Format the time since the input timestamp in a human readable way """
    now = datetime.datetime.fromtimestamp(time.time())
    prev = datetime.datetime.fromtimestamp(timestamp)
    rd = dateutil.relativedelta.relativedelta(now, prev)

    for n, unit in [(rd.years, "year"), (rd.days, "day"), (rd.hours, "hour"),
                    (rd.minutes, "minute")]:
        if n == 1:
            return "{} {} ago".format(n, unit)
        elif n > 1:
            return "{} {}s ago".format(n, unit)
    return "just now"


if __name__ == '__main__':
    # register format_duration for use in html template
    app.jinja_env.globals.update(format_duration=format_duration)

    # start Flask server
    # Flask's debug mode is unrelated to ptvsd debugger used by Cloud Code
    app.run(debug=False, port=PORT, host=HOST)
