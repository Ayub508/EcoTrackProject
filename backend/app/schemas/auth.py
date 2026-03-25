from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
    display_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    country_code = fields.String(validate=validate.Length(max=3), load_default='GB')


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
