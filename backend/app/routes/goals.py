from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models import Goal
from app.schemas import GoalSchema
from app.services.goal_service import compute_goal_progress

goals_bp = Blueprint('goals', __name__)
goal_schema = GoalSchema()


@goals_bp.route('', methods=['POST'])
@jwt_required()
def create_goal():
    try:
        data = goal_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

    user_id = int(get_jwt_identity())
    goal = Goal(
        user_id=user_id,
        title=data['title'],
        category=data.get('category'),
        target_co2_kg=data['target_co2_kg'],
        period=data.get('period', 'weekly'),
        start_date=data['start_date'],
        end_date=data.get('end_date')
    )

    db.session.add(goal)
    db.session.commit()
    return jsonify({'goal': goal.to_dict()}), 201


@goals_bp.route('', methods=['GET'])
@jwt_required()
def list_goals():
    user_id = int(get_jwt_identity())
    status = request.args.get('status', 'active')

    query = Goal.query.filter_by(user_id=user_id)
    if status != 'all':
        query = query.filter_by(status=status)

    goals = query.order_by(Goal.created_at.desc()).all()

    for goal in goals:
        compute_goal_progress(goal)
    db.session.commit()

    return jsonify({'goals': [g.to_dict() for g in goals]}), 200


@goals_bp.route('/<int:goal_id>', methods=['GET'])
@jwt_required()
def get_goal(goal_id):
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404

    compute_goal_progress(goal)
    db.session.commit()
    return jsonify({'goal': goal.to_dict()}), 200


@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404

    data = request.get_json()
    if 'title' in data:
        goal.title = data['title']
    if 'target_co2_kg' in data:
        goal.target_co2_kg = data['target_co2_kg']
    if 'status' in data:
        goal.status = data['status']
    if 'end_date' in data:
        goal.end_date = data['end_date']

    db.session.commit()
    return jsonify({'goal': goal.to_dict()}), 200


@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    user_id = int(get_jwt_identity())
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404

    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted'}), 200
