import base64
import json
import logging
import os

from flask import current_app, Flask, render_template, request, redirect
from google.cloud import pubsub_v1
import requests


app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.
app.config['TOKEN'] = os.environ['TOKEN']

# Global list to storage messages received by this instance.
PUBSUB_MESSAGES = []
SNS_MESSAGES = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', pubsub_messages=PUBSUB_MESSAGES,
                               sns_messages=SNS_MESSAGES)

    return 'OK', 200


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    PUBSUB_MESSAGES.clear()
    SNS_MESSAGES.clear()
    return redirect("/", code=302)

def extract_image(message):
    mj = json.loads(message)
    img = mj['mediaLink']
    return img


@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    if (request.args.get('token', '') !=
            current_app.config['TOKEN']):
        return 'Invalid request', 400

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])

    print("Got Pub/Sub message: ", payload)
    PUBSUB_MESSAGES.append(extract_image(payload))

    return 'OK', 200


@app.route('/sns/push', methods = ['GET', 'POST', 'PUT'])
def sns():
    if (request.args.get('token', '') !=
            current_app.config['TOKEN']):
        return 'Invalid request', 400

    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        r = requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        print("Appending SNS message", js["Message"])
        SNS_MESSAGES.append(extract_image(js['Message']))

    return 'OK\n'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
