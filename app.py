
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import crawler
from config import *

app = Flask(__name__)
CORS(app)


@app.route('/get-job', methods=['POST'])
def get_job():
    # receive parameters
    result_list = request.json


    # call crawler
    results = crawler.Crawler().run(result_list)

    # return json response
    response = {'results': results}
    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", API_PORT))
    app.run(debug=API_DEBUG, host='0.0.0.0', port=port)
