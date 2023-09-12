from marshmallow import Schema, fields

#Create user schema
class UserSchema(Schema):
    name = fields.String(required=True, validate=lambda x: len(x) > 2)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=lambda x: len(x) >= 8)

#Update user schema
class UpdateSchema(Schema):
    name = fields.String(validate=lambda x: len(x) > 0)
    email = fields.Email()
    password = fields.String(validate=lambda x: len(x) >=8)