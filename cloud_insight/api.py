from flask import Flask, request
from flask_cors import CORS
import json
import cloud_insight.executor as executor

flask_app = Flask(__name__)
cors = CORS(flask_app, resources={r"/*": {"origins": "*"}})


def start_api(app):
    app.log.info('Starting the API')

    @flask_app.route("/list", methods=['POST'])
    def list_route():
        if request.method == 'POST':
            app.config.merge(
                json.loads(
                    request.data
                )
            )
            json_services = json.dumps(
                executor.main(app, 'list'),
                indent=4,
                sort_keys=True,
                default=str
            )
            return json_services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    flask_app.run(debug=True)
