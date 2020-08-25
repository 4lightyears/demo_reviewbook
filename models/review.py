from extensions import db

review_list = []

def get_last_id():
    if review_list:
        last_review = review_list[-1]
    else:
        return 1
    return last_review.id + 1

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String(300))
    book_name = db.Column(db.String(300))
    is_publish = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @property
    def data(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'body': self.body,
            'book_name': self.book_name
        }