from marshmallow import Schema, fields, validate

VALID_CATEGORIES = ['transport', 'energy', 'diet', 'consumption']


class ActivitySchema(Schema):
    category = fields.String(required=True, validate=validate.OneOf(VALID_CATEGORIES))
    sub_category = fields.String(required=True, validate=validate.Length(min=1, max=100))
    quantity = fields.Float(required=True, validate=validate.Range(min=0))
    unit = fields.String(required=True, validate=validate.Length(min=1, max=50))
    date = fields.Date(required=True)
    notes = fields.String(validate=validate.Length(max=500), load_default=None)
    emission_factor_id = fields.Integer(load_default=None)
