from sqlalchemy import asc, desc, or_

from extensions import db


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String())
    book_name = db.Column(db.String())
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all(cls, q, sort, order):
        key = '%{keyword}%'.format(keyword=q)
        if order == 'asc':
            sort_type = asc(getattr(cls, sort))
        else:
            sort_type = desc(getattr(cls, sort))


        all_queries = cls.query.filter(or_(cls.book_name.ilike(key), cls.body.ilike(key))).order_by(sort_type)
        return all_queries

    @classmethod
    def get_by_id(cls, review_id):
        return cls.query.filter_by(id=review_id).first()
    
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
