from datetime import datetime, timezone
from app.extensions import db


class BehaviourLog(db.Model):
    __tablename__ = 'behaviour_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    week_start = db.Column(db.Date, nullable=False)
    transport_co2 = db.Column(db.Float, default=0.0)
    energy_co2 = db.Column(db.Float, default=0.0)
    diet_co2 = db.Column(db.Float, default=0.0)
    consumption_co2 = db.Column(db.Float, default=0.0)
    total_co2 = db.Column(db.Float, default=0.0)
    behaviour_class = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'week_start': self.week_start.isoformat() if self.week_start else None,
            'transport_co2': round(self.transport_co2, 3),
            'energy_co2': round(self.energy_co2, 3),
            'diet_co2': round(self.diet_co2, 3),
            'consumption_co2': round(self.consumption_co2, 3),
            'total_co2': round(self.total_co2, 3),
            'behaviour_class': self.behaviour_class,
        }
