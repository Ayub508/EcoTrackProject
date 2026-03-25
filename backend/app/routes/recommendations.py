from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Recommendation, UserRecommendation

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = int(get_jwt_identity())

    try:
        from app.services.ml_service import get_recommendations
        result = get_recommendations(user_id)
        return jsonify(result), 200
    except Exception:
        recs = Recommendation.query.all()
        return jsonify({
            'recommendations': [r.to_dict() for r in recs],
            'behaviour_class': 'unknown'
        }), 200


@recommendations_bp.route('/<int:rec_id>/act', methods=['POST'])
@jwt_required()
def act_on_recommendation(rec_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    action = data.get('action', 'accepted')

    rec = Recommendation.query.get(rec_id)
    if not rec:
        return jsonify({'error': 'Recommendation not found'}), 404

    user_rec = UserRecommendation.query.filter_by(
        user_id=user_id, recommendation_id=rec_id
    ).first()

    if user_rec:
        user_rec.status = action
    else:
        user_rec = UserRecommendation(
            user_id=user_id,
            recommendation_id=rec_id,
            status=action
        )
        db.session.add(user_rec)

    db.session.commit()
    return jsonify({'message': f'Recommendation {action}', 'user_recommendation': user_rec.to_dict()}), 200
