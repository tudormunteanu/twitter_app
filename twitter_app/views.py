from flask import render_template
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask.ext.login import login_required

from .database import session, Tweet, User
import json
import pandas as pd
from . import app

@app.route("/")   
def homepage():
    db_tweet = session.query(Tweet).all()
    db_tweet_location = session.query(Tweet.location)
    db_tweet_location_decoded = []
    for item in db_tweet_location:
        db_tweet_location_decoded.append(item)
    print (len(db_tweet))
    return render_template("base.html",db_tweet=db_tweet, db_tweet_location_decoded=db_tweet_location_decoded)

@app.route("/user_lang")
def user_language():
    x = []
    user_language = session.query(Tweet.user_lang)
    for i in user_language:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("user_lang.html", json_data=json_data)

@app.route("/location")
def user_location():
    x = []
    user_location = session.query(Tweet.location)
    for i in user_location:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("location.html", json_data=json_data)

@app.route("/coordinates")
def coordinates():
    x = []
    coordinates = session.query(Tweet.coordinates)
    for i in coordinates:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("coordinates.html", json_data=json_data)

@app.route("/created_at")
def created_at():
    x = []
    created_at = session.query(Tweet.created_at)
    for i in created_at:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("created_at.html", json_data=json_data)

@app.route("/favorite_count")
def favorite_count():
    x = []
    favorite_count = session.query(Tweet.favorite_count)
    for i in favorite_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("favorite_count.html", json_data=json_data)

@app.route("/tweet_lang")
def tweet_language():
    x = []
    tweet_language = session.query(Tweet.tweet_lang)
    for i in tweet_language:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("tweet_lang.html", json_data=json_data)

@app.route("/retweet_count")
def retweet_count():
    x = []
    retweet_count = session.query(Tweet.retweet_count)
    for i in retweet_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("retweet_count.html", json_data=json_data)

@app.route("/text")
def text():
    x = []
    text = session.query(Tweet.text)
    for i in text:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("text.html", json_data=json_data)

@app.route("/hashtag")
def hashtag():
    x = []
    hashtag = session.query(Tweet.hashtag)
    for i in hashtag:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("hashtag.html", json_data=json_data)

# #@app.route("/results/<job_key>", methods = ['GET'])
#     # need to render templates, build template file
#     # need to have the view stream stop after a certain number of tweets
# #def get_results(job_key):

#     #job = Job.fetch(job_key, connection=Redis())

#     #if job.is_finished:
#         return str(job.result), 200
#     else:
#         return "Nay!", 202


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('login.html'))

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))