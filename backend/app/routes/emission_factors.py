from flask import Blueprint, request, jsonify
from app.models import EmissionFactor

emission_factors_bp = Blueprint('emission_factors', __name__)


@emission_factors_bp.route('', methods=['GET'])
def list_emission_factors():
    category = request.args.get('category')
    search = request.args.get('search')

    query = EmissionFactor.query
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            EmissionFactor.sub_category.ilike(f'%{search}%')
        )

    factors = query.order_by(EmissionFactor.category, EmissionFactor.sub_category).all()
    return jsonify({'emission_factors': [f.to_dict() for f in factors]}), 200


@emission_factors_bp.route('/<int:factor_id>', methods=['GET'])
def get_emission_factor(factor_id):
    factor = EmissionFactor.query.get(factor_id)
    if not factor:
        return jsonify({'error': 'Emission factor not found'}), 404
    return jsonify({'emission_factor': factor.to_dict()}), 200
