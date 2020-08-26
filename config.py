class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://varun_reviewbook:sharma@localhost/reviewbook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'