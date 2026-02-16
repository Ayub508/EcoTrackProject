import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_synthetic_data_generation():
    from ml.data.synthetic_training import generate_synthetic_data
    df = generate_synthetic_data(n_users=10, n_weeks=10)
    assert len(df) == 100  # 10 users * 10 weeks
    assert 'transport_co2' in df.columns
    assert 'behaviour_class' in df.columns
    assert df['total_co2'].min() >= 0


def test_prediction_features_creation():
    from ml.data.synthetic_training import generate_synthetic_data, create_prediction_features
    df = generate_synthetic_data(n_users=5, n_weeks=10)
    features = create_prediction_features(df)
    assert len(features) > 0
    assert 'transport_avg_4w' in features.columns
    assert 'target_co2' in features.columns


def test_classification_features_creation():
    from ml.data.synthetic_training import generate_synthetic_data, create_classification_features
    df = generate_synthetic_data(n_users=5, n_weeks=10)
    features = create_classification_features(df)
    assert len(features) > 0
    assert 'transport_pct' in features.columns
    assert 'behaviour_class' in features.columns


def test_recommendation_scoring():
    from ml.recommendation_engine import score_recommendations

    recs = [
        {'id': 1, 'title': 'Cycle more', 'category': 'transport', 'potential_co2_saved_kg': 7.5, 'difficulty': 'medium'},
        {'id': 2, 'title': 'LED bulbs', 'category': 'energy', 'potential_co2_saved_kg': 3.0, 'difficulty': 'easy'},
        {'id': 3, 'title': 'Eat less beef', 'category': 'diet', 'potential_co2_saved_kg': 10.0, 'difficulty': 'medium'},
    ]

    scored = score_recommendations(recs, 'high_transport', {}, set())
    assert len(scored) == 3
    assert scored[0]['score'] >= scored[1]['score']
    assert all('score' in r for r in scored)
    assert all('score_breakdown' in r for r in scored)

    # Transport recommendations should score higher for high_transport users
    transport_scores = [r['score'] for r in scored if r['category'] == 'transport']
    energy_scores = [r['score'] for r in scored if r['category'] == 'energy']
    if transport_scores and energy_scores:
        assert max(transport_scores) >= max(energy_scores)


def test_recommendation_novelty_penalty():
    from ml.recommendation_engine import score_recommendations

    recs = [
        {'id': 1, 'title': 'Cycle more', 'category': 'transport', 'potential_co2_saved_kg': 7.5, 'difficulty': 'medium'},
    ]

    scored_new = score_recommendations(recs, 'balanced_high', {}, set())
    scored_old = score_recommendations(recs, 'balanced_high', {}, {1})

    assert scored_new[0]['score'] > scored_old[0]['score']
