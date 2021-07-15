
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import crawler
from config import *

app = Flask(__name__)
CORS(app)


@app.route('/get-job', methods=['GET'])
def get_job():
    params = request.args
    job_urls = []
    for key, value in params.items():
        job_urls.append(value)

    results = crawler.Crawler().run(job_urls)

    response = {'results': results, 'success': True, 'msg': "Results obtained", 'error_code': 0}
    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", API_PORT))
    app.run(debug=API_DEBUG, host='0.0.0.0', port=port)
