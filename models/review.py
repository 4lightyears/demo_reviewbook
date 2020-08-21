review_list = []

def get_last_id():
    if review_list:
        last_review = review_list[-1]
    else:
        return 1
    return last_review.id + 1

class Review:
    def __init__(self, rating, body, book_name):
        self.id = get_last_id()
        self.rating = rating
        self.body = body
        self.book_name = book_name
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'body': self.body,
            'book_name': self.book_name
        }