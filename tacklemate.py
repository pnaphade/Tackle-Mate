#!/usr/bin/env python
import os
import flask
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
    print("Received upload request in python server")
    f = flask.request.files['static_file']
    f.save(f.filename)
    print("Successfully saved file", f.filename)
    #formula(f.filename)
    resp = {"success": True, "response": "file saved!", "filename": f.filename}
    return flask.jsonify(resp), 200

@app.route('/get_scores', methods=['GET', 'POST'])
def get_scores():
    username = auth.authenticate()
    given = flask.session.get('given_name')

    video_fn = flask.request.args.get("fn")
    timestamp = flask.request.args.get("timestamp")
    print("Video filename", video_fn)
    print("Tackle timestamp:", timestamp)

    # Calculate the tackle score
    frames = formula.score(video_fn)

    html_code = flask.render_template('results.html', username=username,
            given=given, video_fn=video_fn, timestamp=timestamp, frames=frames)
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
