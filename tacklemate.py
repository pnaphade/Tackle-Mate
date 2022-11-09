#!/usr/bin/env python

import flask
import urllib.parse as up

# database_url = "postgres://

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    html_code = flask.render_template('404.html')
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True)
