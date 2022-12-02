#!/usr/bin/env python
import os
import flask
import urllib.parse as up
import auth

database_url = "postgres://nyodofai:wZThMXsX6hbgqr5PNbgN93kkDA9P3SAo@peanut.db.elephantsql.com/nyodofai"

app = flask.Flask(__name__, template_folder='static/templates')
app.secret_key = os.environ['APP_SECRET_KEY']

#----------------------------------------------------------------------

# Routes for authentication

@app.route('/login', methods=['GET'])
def login():
    return auth.login()

@app.route('/login/callback', methods=['GET'])
def callback():
    return auth.callback()

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutgoogle', methods=['GET'])
def logoutgoogle():
    return auth.logoutgoogle()

#----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #username = "Priya"
    username = auth.authenticate()
    html_code = flask.render_template('index.html', username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/stats', methods=['GET'])
def stats():
    #username = "Priya"
    username = auth.authenticate()
    html_code = flask.render_template('stats.html', username=username)
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    #username = "Priya"
    username = auth.authenticate()
    html_code = flask.render_template('404.html', username=username)
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
