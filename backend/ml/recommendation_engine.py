import numpy as np


def score_recommendations(recommendations, behaviour_class, category_breakdown, accepted_ids=None):
    if accepted_ids is None:
        accepted_ids = set()

    category_weights = {
        'high_transport': {'transport': 2.0, 'energy': 0.8, 'diet': 0.8, 'consumption': 0.7},
        'high_energy': {'transport': 0.8, 'energy': 2.0, 'diet': 0.8, 'consumption': 0.7},
        'high_diet': {'transport': 0.8, 'energy': 0.8, 'diet': 2.0, 'consumption': 0.7},
        'balanced_high': {'transport': 1.2, 'energy': 1.2, 'diet': 1.2, 'consumption': 1.0},
        'improving': {'transport': 1.0, 'energy': 1.0, 'diet': 1.0, 'consumption': 1.0},
    }

    weights = category_weights.get(behaviour_class, category_weights['balanced_high'])

    difficulty_scores = {'easy': 1.0, 'medium': 0.7, 'hard': 0.4}

    scored = []
    for rec in recommendations:
        rec_dict = rec if isinstance(rec, dict) else rec.to_dict()

        relevance = weights.get(rec_dict['category'], 1.0)

        impact = min(rec_dict.get('potential_co2_saved_kg', 0) / 25.0, 1.0)

        feasibility = difficulty_scores.get(rec_dict.get('difficulty', 'medium'), 0.7)

        novelty = 0.3 if rec_dict['id'] in accepted_ids else 1.0

        score = (relevance * 0.35 + impact * 0.30 + feasibility * 0.20 + novelty * 0.15)

        scored.append({
            **rec_dict,
            'score': round(score, 3),
            'score_breakdown': {
                'relevance': round(relevance, 3),
                'impact': round(impact, 3),
                'feasibility': round(feasibility, 3),
                'novelty': round(novelty, 3),
            }
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:10]
