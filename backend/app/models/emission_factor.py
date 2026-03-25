from app.extensions import db


class EmissionFactor(db.Model):
    __tablename__ = 'emission_factors'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    sub_category = db.Column(db.String(100), nullable=False)
    factor_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(200))
    source_url = db.Column(db.String(500))
    region = db.Column(db.String(50), default='Global')
    year = db.Column(db.Integer)
    methodology = db.Column(db.Text)

    activities = db.relationship('Activity', backref='emission_factor', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'sub_category': self.sub_category,
            'factor_value': self.factor_value,
            'unit': self.unit,
            'source': self.source,
            'source_url': self.source_url,
            'region': self.region,
            'year': self.year,
            'methodology': self.methodology,
        }
