from app.extensions import db


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    potential_co2_saved_kg = db.Column(db.Float, default=0.0)
    difficulty = db.Column(db.String(20), default='medium')
    mao_motivation = db.Column(db.Text)
    mao_ability = db.Column(db.Text)
    mao_opportunity = db.Column(db.Text)
    tags = db.Column(db.String(500))

    user_recommendations = db.relationship('UserRecommendation', backref='recommendation', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'potential_co2_saved_kg': self.potential_co2_saved_kg,
            'difficulty': self.difficulty,
            'mao_motivation': self.mao_motivation,
            'mao_ability': self.mao_ability,
            'mao_opportunity': self.mao_opportunity,
            'tags': self.tags.split(',') if self.tags else [],
        }
