import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/otp/send', methods=['POST'])
def send():
    return request.json


app.run()
