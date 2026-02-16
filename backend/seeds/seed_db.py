import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.extensions import db
from app.models import EmissionFactor, Recommendation


def seed_emission_factors():
    data_path = os.path.join(os.path.dirname(__file__), 'emission_factors.json')
    with open(data_path, 'r') as f:
        factors = json.load(f)

    count = 0
    for factor_data in factors:
        existing = EmissionFactor.query.filter_by(
            category=factor_data['category'],
            sub_category=factor_data['sub_category']
        ).first()

        if not existing:
            factor = EmissionFactor(**factor_data)
            db.session.add(factor)
            count += 1

    db.session.commit()
    print(f"Seeded {count} emission factors")


def seed_recommendations():
    data_path = os.path.join(os.path.dirname(__file__), 'recommendations.json')
    with open(data_path, 'r') as f:
        recs = json.load(f)

    count = 0
    for rec_data in recs:
        existing = Recommendation.query.filter_by(title=rec_data['title']).first()
        if not existing:
            rec = Recommendation(**rec_data)
            db.session.add(rec)
            count += 1

    db.session.commit()
    print(f"Seeded {count} recommendations")


def seed_all():
    app = create_app('development')
    with app.app_context():
        db.create_all()
        seed_emission_factors()
        seed_recommendations()
        print("Database seeding complete!")


if __name__ == '__main__':
    seed_all()
