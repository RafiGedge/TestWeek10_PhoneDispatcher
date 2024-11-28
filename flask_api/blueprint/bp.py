import logging
from flask import Blueprint, request, jsonify, current_app

from database.neo4j_service import DeviceDetails

app_bp = Blueprint('app_bp', __name__)


@app_bp.route('/api/phone_tracker', methods=['POST'])
def phone_tracker():
    data = request.json
    print(data)
    try:
        repo = DeviceDetails(current_app.neo4j_driver)
        transaction_id = repo.create_data(data)

        return jsonify({
            'status': 'success',
            'transaction_id': transaction_id
        }), 201

    except Exception as e:
        print(f'Error in POST /api/v1/transaction: {str(e)}')
        logging.error(f'Error in POST /api/v1/transaction: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500
