from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.dashboard_service import get_summary, get_trend

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    user_id = int(get_jwt_identity())
    period = request.args.get('period', 'week')
    data = get_summary(user_id, period)
    return jsonify(data), 200


@dashboard_bp.route('/trend', methods=['GET'])
@jwt_required()
def trend():
    user_id = int(get_jwt_identity())
    weeks = request.args.get('weeks', 12, type=int)
    data = get_trend(user_id, weeks)
    return jsonify({'trend': data}), 200


@dashboard_bp.route('/prediction', methods=['GET'])
@jwt_required()
def prediction():
    user_id = int(get_jwt_identity())
    try:
        from app.services.ml_service import get_prediction
        result = get_prediction(user_id)
        return jsonify(result), 200
    except Exception:
        return jsonify({
            'predicted_co2_kg': None,
            'message': 'Not enough data for prediction'
        }), 200
