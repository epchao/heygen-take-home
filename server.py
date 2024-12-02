"""
You will be writing a server that implements a status API.

It returns a result that is pending, completed or error. 
This is just simulating the video translation backend. 
It will return pending until a configurable time has passed.
"""
import time
from flask import Flask, jsonify

app = Flask(__name__)

START_TIME = time.time()
DELAY_TIME = 10


@app.route('/status')
def get_status():
    """
    GET /status endpoint
    Return result with {“result”: “pending” or “error” or “completed”}.
    """
    res = {"result": "", "message": ""}
    try:
        elapsed_time = time.time() - START_TIME
        if elapsed_time < DELAY_TIME:
            res['result'] = "pending"
        else:
            res['result'] = "completed"
    except Exception as e: # pylint: disable=broad-except
        res['result'] = "error"
        res['message'] = e

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
