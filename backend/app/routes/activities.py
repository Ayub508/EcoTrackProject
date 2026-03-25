from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models import Activity
from app.schemas import ActivitySchema
from app.services.carbon_calculator import calculate_activity_co2

activities_bp = Blueprint('activities', __name__)
activity_schema = ActivitySchema()


@activities_bp.route('', methods=['POST'])
@jwt_required()
def create_activity():
    try:
        data = activity_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    user_id = int(get_jwt_identity())
    co2_kg, factor_id = calculate_activity_co2(
        data['category'], data['sub_category'],
        data['quantity'], data.get('emission_factor_id')
    )

    activity = Activity(
        user_id=user_id,
        category=data['category'],
        sub_category=data['sub_category'],
        quantity=data['quantity'],
        unit=data['unit'],
        emission_factor_id=factor_id,
        co2_kg=co2_kg,
        date=data['date'],
        notes=data.get('notes')
    )

    db.session.add(activity)
    db.session.commit()
    return jsonify({'activity': activity.to_dict()}), 201


@activities_bp.route('', methods=['GET'])
@jwt_required()
def list_activities():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')

    query = Activity.query.filter_by(user_id=user_id)
    if category:
        query = query.filter_by(category=category)

    query = query.order_by(Activity.date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'activities': [a.to_dict() for a in pagination.items],
        'total': pagination.total,
        'page': page,
        'pages': pagination.pages
    }), 200


@activities_bp.route('/<int:activity_id>', methods=['GET'])
@jwt_required()
def get_activity(activity_id):
    user_id = int(get_jwt_identity())
    activity = Activity.query.filter_by(id=activity_id, user_id=user_id).first()
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    return jsonify({'activity': activity.to_dict()}), 200


@activities_bp.route('/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    user_id = int(get_jwt_identity())
    activity = Activity.query.filter_by(id=activity_id, user_id=user_id).first()
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    try:
        data = activity_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    co2_kg, factor_id = calculate_activity_co2(
        data['category'], data['sub_category'],
        data['quantity'], data.get('emission_factor_id')
    )

    activity.category = data['category']
    activity.sub_category = data['sub_category']
    activity.quantity = data['quantity']
    activity.unit = data['unit']
    activity.emission_factor_id = factor_id
    activity.co2_kg = co2_kg
    activity.date = data['date']
    activity.notes = data.get('notes')

    db.session.commit()
    return jsonify({'activity': activity.to_dict()}), 200


@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    user_id = int(get_jwt_identity())
    activity = Activity.query.filter_by(id=activity_id, user_id=user_id).first()
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    db.session.delete(activity)
    db.session.commit()
    return jsonify({'message': 'Activity deleted'}), 200
