from datetime import datetime, timezone
from app.extensions import db


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    emission_factor_id = db.Column(db.Integer, db.ForeignKey('emission_factors.id'))
    co2_kg = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category': self.category,
            'sub_category': self.sub_category,
            'quantity': self.quantity,
            'unit': self.unit,
            'emission_factor_id': self.emission_factor_id,
            'co2_kg': round(self.co2_kg, 3),
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
