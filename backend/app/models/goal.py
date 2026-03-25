from datetime import datetime, timezone
from app.extensions import db


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    target_co2_kg = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), default='weekly')
    current_co2_kg = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        progress = 0
        if self.target_co2_kg > 0:
            progress = round(min((self.current_co2_kg / self.target_co2_kg) * 100, 100), 1)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'category': self.category,
            'target_co2_kg': self.target_co2_kg,
            'period': self.period,
            'current_co2_kg': round(self.current_co2_kg, 3),
            'status': self.status,
            'progress': progress,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
