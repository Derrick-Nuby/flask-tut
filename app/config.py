import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://derrickuser:123@localhost/derricktest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SECRET_KEY = 'AI WILL RULE THE DAY'
