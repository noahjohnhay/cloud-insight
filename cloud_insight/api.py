import json
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

    @flask_app.route("/compare", methods=['POST'])
    def compare_route():
        if request.method == 'POST':
            services = post_handler(app, 'compare')
            return services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/connectivity", methods=['POST'])
    def connectivity_route():
        if request.method == 'POST':
            services = post_handler(app, 'connectivity')
            return services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/health", methods=['POST'])
    def health_route():
        if request.method == 'POST':
            services = post_handler(app, 'health')
            return services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/history", methods=['POST'])
    def history_route():
        if request.method == 'POST':
            services = post_handler(app, 'history')
            return services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    @flask_app.route("/list", methods=['POST'])
    def list_route():
        if request.method == 'POST':
            services = post_handler(app, 'list')
            return services, 201
        else:
            app.log.error('Invalid Method')
            return 'INVALID METHOD', 404

    flask_app.run(
        debug=False
    )
