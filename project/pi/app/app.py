from flask import Flask, make_response

from app.metrics import generate_metrics

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/node/<path:node>/metrics')
def metrics(node):
    response = make_response(generate_metrics(node), 200)
    response.mimetype = "text/plain"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
