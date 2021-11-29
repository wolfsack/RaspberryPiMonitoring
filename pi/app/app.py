from flask import Flask, make_response

from app.metrics import generate_metrics

# create Flask App
app = Flask(__name__)


# define HTTP endpoint
@app.route('/node/<path:node>/metrics')
def metrics(node):
    # create response with a body containing metrics as string  and status-code 200
    response = make_response(generate_metrics(node), 200)

    # set response type to text/plain
    # important because prometheus needs plain text to parse the data correctly
    response.mimetype = "text/plain"

    # send response
    return response


# only for testing purpose
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
