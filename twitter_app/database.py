from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from flask.ext.login import UserMixin
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# This is the table to store users who signup to the website to access the app
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

# This is the table that stores the information we want form the tweets
class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    location = Column(String(128))
    user_lang = Column(String(128))
    coordinates = Column(String(128), nullable = True)
    created_at = Column(String(128))
    favorite_count = Column(Integer, nullable = True)
    tweet_lang = Column(String(128), nullable = True)
    retweet_count = Column(Integer, nullable = True)
    text = Column(String(128))
    hashtag = Column(String(128), nullable = True)
    
Base.metadata.create_all(engine)