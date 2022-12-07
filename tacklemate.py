#!/usr/bin/env python
import os
import flask
import urllib.parse as up
import auth
import formula

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
    username = auth.authenticate()
    given = flask.session.get('given_name')
    html_code = flask.render_template('index.html', username=username,
                                    given=given)
    response = flask.make_response(html_code)

    return response

@app.route('/upload_static_file', methods=['POST'])
def upload_static_file():
    print("Got request in static files")
    print(flask.request.files)
    f = flask.request.files['static_file']
    f.save(f.filename)
    resp = {"success": True, "response": "file saved!"}
    return flask.jsonify(resp), 200

@app.route('/get_scores', methods=['POST'])
def get_scores():
    print("in get_scores python function")
    username = auth.authenticate()
    given = flask.session.get('given_name')

    # Get data embedded in the post request body
    data = flask.request.json
    video = data["video"]
    # timestamp = data['timestamp']
    print("Type of video:", type(video))
    print(len(video))
    #write each character of string into file, then put file into algorithm

    video_bytes = video.encode('utf-8')
    print("hello")
    with open('testfile.mp4', 'wb') as wfile:
        wfile.write(video_bytes)
    print("hello2")

    # print(timestamp)



    # Get form inputs
    '''
    vid = flask.request.form.get("vid")
    side = flask.request.form.get("side")
    print("Read video filename:", vid)
    print("type of vid:", type(vid))
    print("Tackle side:", side)
    '''

    # Calculate the tackle score
    #scores = formula.score(vid)

    html_code = flask.render_template('results.html', username=username,
                                    given=given)
    response = flask.make_response(html_code)
    return response



@app.route('/stats', methods=['GET'])
def stats():
    username = auth.authenticate()
    given = flask.session.get('given_name')
    html_code = flask.render_template('stats.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    given = flask.session.get('given_name')
    html_code = flask.render_template('404.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
