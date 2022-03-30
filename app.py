
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import MainCrawler
from config import *
import json

app = Flask(__name__)
CORS(app)


@app.route('/get-job', methods=['POST'])
def get_job():
    try:
        results_dict = {
            "error_code": None,
            "msg": None,
            "results": None
        }

        # receive parameters
        result_list = request.json

        # call crawler
        results_list = MainCrawler.Crawler().run(result_list)
        
        results_dict['error_code'] = 0
        results_dict['msg'] = "Results obtained"
        results_dict['results'] = results_list

        response = app.response_class(
            response=json.dumps(results_dict),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        results_dict['error_code'] = e.code
        results_dict['msg'] = f"Error found on app.py::get_job method: {e.description}; Check the body content for the POST requests"
        results_dict['results'] = None

        response = app.response_class(
            response=json.dumps(results_dict),
            status=e.code,
            mimetype='application/json'
        )
    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", API_PORT))
    app.run(debug=API_DEBUG, host='0.0.0.0', port=port)
