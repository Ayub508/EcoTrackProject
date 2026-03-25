from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(3), default='GB')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    goals = db.relationship('Goal', backref='user', lazy='dynamic')
    behaviour_logs = db.relationship('BehaviourLog', backref='user', lazy='dynamic')
    user_recommendations = db.relationship('UserRecommendation', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'display_name': self.display_name,
            'country_code': self.country_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
