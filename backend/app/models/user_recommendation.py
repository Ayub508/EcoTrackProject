from datetime import datetime, timezone
from app.extensions import db


class UserRecommendation(db.Model):
    __tablename__ = 'user_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_id': self.recommendation_id,
            'score': round(self.score, 3),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
