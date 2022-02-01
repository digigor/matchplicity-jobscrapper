
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import crawler_tk
from config import *

app = Flask(__name__)
CORS(app)


@app.route('/get-job', methods=['POST'])
def get_job():
    try:
        # receive parameters
        result_list = request.json

        # call crawler
        results = crawler_tk.Crawler().run(result_list)

        response = {'success': True, 'data': results}
        return jsonify(response)
    except Exception as e:
        response = {'success': False, 'msg': str(e), 'error_code': 1}
        return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", API_PORT))
    app.run(debug=API_DEBUG, host='0.0.0.0', port=port)
