from . import app

from flask import render_template
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask.ext.login import login_required

from redis import Redis
from rq import Queue
from rq.job import Job

from .database import session, Tweet, User
from .twitter_streaming import Main
import json
import pandas as pd

def get_tweets():
        num_tweets_to_grab = 20
        program = Main(num_tweets_to_grab)
        program.get_streaming_data()

@app.route("/")   
def homepage():
    q = Queue(connection=Redis())
    results = q.enqueue(get_tweets, result_ttl=5000)
    db_tweet = session.query(Tweet)
    tweet_text = db_tweet.text
    tweet_id = db_tweet.tweet_lang
    print (db_tweet)
    print(results.get_id())
    return render_template("base.html",results=results,tweet_id=tweet_id,tweet_text=tweet_text)

@app.route("/results/<job_key>", methods = ['GET'])
    # need to render templates, build template file
    # need to have the view stream stop after a certain number of tweets
def get_results(job_key):

    job = Job.fetch(job_key, connection=Redis())

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202


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