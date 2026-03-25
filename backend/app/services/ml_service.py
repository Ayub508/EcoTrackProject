import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import func

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.extensions import db
from app.models import Activity, Recommendation, UserRecommendation, BehaviourLog


def _get_user_weekly_data(user_id, weeks=4):
    now = datetime.utcnow().date()
    start = now - timedelta(weeks=weeks)

    results = db.session.query(
        func.strftime('%Y-%W', Activity.date).label('week'),
        Activity.category,
        func.sum(Activity.co2_kg).label('total_co2')
    ).filter(
        Activity.user_id == user_id,
        Activity.date >= start
    ).group_by('week', Activity.category).all()

    weekly = {}
    for row in results:
        week_str = str(row.week)
        if week_str not in weekly:
            weekly[week_str] = {'transport': 0, 'energy': 0, 'diet': 0, 'consumption': 0, 'total': 0}
        weekly[week_str][row.category] = float(row.total_co2)
        weekly[week_str]['total'] += float(row.total_co2)

    return list(weekly.values())


def _build_prediction_features(weekly_data):
    if len(weekly_data) < 4:
        return None

    recent = weekly_data[-4:]
    import numpy as np

    features = {
        'transport_avg_4w': np.mean([w['transport'] for w in recent]),
        'energy_avg_4w': np.mean([w['energy'] for w in recent]),
        'diet_avg_4w': np.mean([w['diet'] for w in recent]),
        'consumption_avg_4w': np.mean([w['consumption'] for w in recent]),
        'total_avg_4w': np.mean([w['total'] for w in recent]),
        'transport_change': (recent[-1]['transport'] - recent[0]['transport']) / max(recent[0]['transport'], 0.1),
        'energy_change': (recent[-1]['energy'] - recent[0]['energy']) / max(recent[0]['energy'], 0.1),
        'diet_change': (recent[-1]['diet'] - recent[0]['diet']) / max(recent[0]['diet'], 0.1),
        'consumption_change': (recent[-1]['consumption'] - recent[0]['consumption']) / max(recent[0]['consumption'], 0.1),
        'total_change': (recent[-1]['total'] - recent[0]['total']) / max(recent[0]['total'], 0.1),
        'month': datetime.utcnow().month,
        'activity_frequency': 4,
    }
    return features


def _build_classification_features(weekly_data):
    if len(weekly_data) < 4:
        return None

    import numpy as np
    recent = weekly_data[-4:]
    total = np.mean([w['total'] for w in recent])
    if total == 0:
        total = 0.01

    features = {
        'transport_pct': np.mean([w['transport'] for w in recent]) / total,
        'energy_pct': np.mean([w['energy'] for w in recent]) / total,
        'diet_pct': np.mean([w['diet'] for w in recent]) / total,
        'consumption_pct': np.mean([w['consumption'] for w in recent]) / total,
        'transport_trend': 1 if recent[-1]['transport'] > recent[0]['transport'] else -1,
        'energy_trend': 1 if recent[-1]['energy'] > recent[0]['energy'] else -1,
        'diet_trend': 1 if recent[-1]['diet'] > recent[0]['diet'] else -1,
        'total_vs_avg_ratio': total / 50.0,
    }
    return features


def get_prediction(user_id):
    weekly_data = _get_user_weekly_data(user_id)
    features = _build_prediction_features(weekly_data)

    if features is None:
        return {'predicted_co2_kg': None, 'message': 'Need at least 4 weeks of data'}

    try:
        from ml.carbon_predictor import predict
        predicted = predict(features)
        return {
            'predicted_co2_kg': round(predicted, 2),
            'message': 'Prediction based on your last 4 weeks of activity'
        }
    except FileNotFoundError:
        return {'predicted_co2_kg': None, 'message': 'ML model not trained yet'}


def get_behaviour_class(user_id):
    weekly_data = _get_user_weekly_data(user_id)
    features = _build_classification_features(weekly_data)

    if features is None:
        return 'balanced_high', {}

    try:
        from ml.behaviour_classifier import classify
        label, probs = classify(features)
        return label, probs
    except FileNotFoundError:
        return 'balanced_high', {}


def get_recommendations(user_id):
    behaviour_class, probs = get_behaviour_class(user_id)

    weekly_data = _get_user_weekly_data(user_id)
    if weekly_data:
        import numpy as np
        recent = weekly_data[-4:] if len(weekly_data) >= 4 else weekly_data
        category_breakdown = {
            'transport': np.mean([w['transport'] for w in recent]),
            'energy': np.mean([w['energy'] for w in recent]),
            'diet': np.mean([w['diet'] for w in recent]),
            'consumption': np.mean([w['consumption'] for w in recent]),
        }
    else:
        category_breakdown = {'transport': 0, 'energy': 0, 'diet': 0, 'consumption': 0}

    accepted = UserRecommendation.query.filter_by(
        user_id=user_id, status='accepted'
    ).all()
    accepted_ids = {ur.recommendation_id for ur in accepted}

    all_recs = Recommendation.query.all()

    from ml.recommendation_engine import score_recommendations
    scored = score_recommendations(all_recs, behaviour_class, category_breakdown, accepted_ids)

    return {
        'recommendations': scored,
        'behaviour_class': behaviour_class,
        'category_breakdown': category_breakdown,
    }
