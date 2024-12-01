import logging
from flask import Blueprint, request, jsonify, current_app

from service.neo4j_service import Neo4jService

app_bp = Blueprint('app_bp', __name__, url_prefix='/api')


@app_bp.route('/phone_tracker', methods=['POST'])
def phone_tracker():
    data = request.json
    print(data)
    try:
        db = Neo4jService(current_app.neo4j_driver)
        devices_result = db.insert_devices(data['devices'])
        interaction_result = db.create_interaction(data['interaction'])

        return jsonify({"devices": devices_result, "interaction": interaction_result}), 201

    except Exception as e:
        print(f'Error in POST /api/phone_tracker: {e}')
        logging.error(e)
        return jsonify({'error': 'internal server error'}), 500


@app_bp.route('/bluetooth_path', methods=['GET'])
def devices_by_bluetooth():
    try:
        db = Neo4jService(current_app.neo4j_driver)
        result = db.get_by_bluetooth()
        return jsonify(result), 200
    except Exception as e:
        print(f'Error in POST /api/bluetooth_path: {e}')
        logging.error(e)
        return jsonify({'error': 'internal server error'}), 500


@app_bp.route('/stronger_signal/<signal_strength>', methods=['GET'])
def devices_by_stronger_signal(signal_strength):
    try:
        db = Neo4jService(current_app.neo4j_driver)
        result = db.get_by_stronger_than(int(signal_strength))
        return jsonify(result), 200
    except Exception as e:
        print(f'Error in GET /api/stronger_signal: {e}')
        logging.error(e)
        return jsonify({'error': 'internal server error'}), 500


@app_bp.route('/connected_count/<string:device_id>', methods=['GET'])
def devices_connected(device_id):
    try:
        db = Neo4jService(current_app.neo4j_driver)
        result = db.get_devices_connected(device_id)
        return jsonify(result), 200
    except Exception as e:
        print(f'Error in GET /api/connected_count: {e}')
        logging.error(e)
        return jsonify({'error': 'internal server error'}), 500


@app_bp.route('/direct_connection', methods=['GET'])
def check_direct_connection():
    from_device_id = request.args.get('from_device_id')
    to_device_id = request.args.get('to_device_id')
    try:
        db = Neo4jService(current_app.neo4j_driver)
        result = db.check_direct_connection(from_device_id, to_device_id)
        return jsonify(result), 200
    except Exception as e:
        print(f'Error in GET /api/direct_connection: {e}')
        logging.error(e)
        return jsonify({'error': 'internal server error'}), 500
