from marshmallow import Schema, fields, validate, post_dump

from schemas.user import UserSchema

class ReviewSchema(Schema):
    class Meta:
        ordered = True
    
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    rating = fields.Integer(required=True)
    body = fields.String(validate=[validate.Length(max=400)])
    book_name = fields.String(validate=[validate.Length(max=100)])
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email',))

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data