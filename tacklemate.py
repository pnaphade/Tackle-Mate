#!/usr/bin/env python
import os
import flask
import tensorflow_hub as hub
import auth
import formula

model =  None
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
    timestamp = float(flask.request.args.get("timestamp"))
    print("Video filename", video_fn)
    print("Tackle timestamp:", timestamp)

    # Calculate the tackle score
    scores, length = formula.score(movenet_model, video_fn, timestamp)
    rating = {0:"poor", 1:"fair", 2:"good", 3:"excellent"}
    h_feeback = \
        {0:"Minimal change in height at tackle. Try to bend the knees \
            and drop the shoulders.",
        1:"Some decrease in height at tackle. Try to drop to where the \
            ball carrier's knees would be.", \
        2:"Good decrease in height at tackle! Try to drop to where the \
            ball carrier's knees would be.",
        3:"Excellent drop in height! As an excercise, try to brush the \
            hands against the ground before making contact."}

    height_score = scores["height"]
    height_rating = rating[height_score]
    height_feedback = h_feeback[height_score]

    html_code = flask.render_template('results.html', username=username,
            given=given, video_fn=video_fn, timestamp=round(timestamp, 2),
            height_score=height_score, height_rating=height_rating,
            height_feedback=height_feedback, length=length)
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

def load_model():
    global movenet_model
    movenet_model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
    movenet_model = movenet_model.signatures['serving_default'] # default model

if __name__ == '__main__':
    load_model()
    app.run(debug=True, ssl_context='adhoc')
