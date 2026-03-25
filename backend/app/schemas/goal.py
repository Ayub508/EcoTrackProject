from marshmallow import Schema, fields, validate


class GoalSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    category = fields.String(validate=validate.Length(max=50), load_default=None)
    target_co2_kg = fields.Float(required=True, validate=validate.Range(min=0))
    period = fields.String(validate=validate.OneOf(['daily', 'weekly', 'monthly']), load_default='weekly')
    start_date = fields.Date(required=True)
    end_date = fields.Date(load_default=None)
