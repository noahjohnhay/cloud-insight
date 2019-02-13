import json
import cloud_insight.aws as aws
import cloud_insight.executor as executor
from flask import Flask, request
from flask_cors import CORS

flask_app = Flask(__name__)
cors = CORS(flask_app, resources={r"/*": {"origins": "*"}})


def post_handler(app, namespace):
    app.config.merge(
        json.loads(
            request.data
        )
    )
    services = json.dumps(
        executor.main(app, namespace),
        indent=4,
        sort_keys=True,
        default=str
    )
    return services


def start_api(app):
    app.log.info('Starting the API')

    @flask_app.route("/", methods=['GET'])
    def default_route():
        return '', 200

    @flask_app.route("/compare", methods=['POST'])
    def compare_route():
        if request.method == 'POST':
            response = flask_app.response_class(
                mimetype='application/json',
                response=post_handler(app, 'compare'),
                status=200
            )
            return response
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/connectivity", methods=['POST'])
    def connectivity_route():
        if request.method == 'POST':
            response = flask_app.response_class(
                mimetype='application/json',
                response=post_handler(app, 'connectivity'),
                status=200
            )
            return response
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/health", methods=['POST'])
    def health_route():
        if request.method == 'POST':
            response = flask_app.response_class(
                mimetype='application/json',
                response=post_handler(app, 'health'),
                status=200
            )
            return response
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/history", methods=['POST'])
    def history_route():
        if request.method == 'POST':
            response = flask_app.response_class(
                mimetype='application/json',
                response=post_handler(app, 'history'),
                status=200
            )
            return response
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/list", methods=['POST'])
    def list_route():
        if request.method == 'POST':
            response = flask_app.response_class(
                mimetype='application/json',
                response=post_handler(app, 'list'),
                status=200
            )
            return response
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/regions", methods=['GET'])
    def regions_route():
        response = flask_app.response_class(
            mimetype='application/json',
            response=json.dumps(
                aws.list_regions(
                    request.args.get('aws_service')
                )
            ),
            status=200
        )
        return response

    flask_app.run(
        host='127.0.0.1',
        port='54321',
        debug=False
    )
