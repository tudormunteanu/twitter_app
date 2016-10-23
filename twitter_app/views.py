import datetime
from flask import render_template
from flask import request, redirect, url_for, Response

from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask.ext.login import login_required

from .database import session, Tweet, User
import json
import pandas as pd
from . import app

from nvd3 import pieChart
from collections import Counter
from collections import defaultdict

@app.route("/")   
def homepage():
    db_tweet = session.query(Tweet).all()
    db_tweet_location = session.query(Tweet.location)
    db_tweet_location_decoded = []
    for item in db_tweet_location:
        db_tweet_location_decoded.append(item)
    print (len(db_tweet))
    return render_template("base.html",db_tweet=db_tweet, db_tweet_location_decoded=db_tweet_location_decoded)

@app.route("/demo")
def demo_chart():
    from nvd3 import pieChart

    # Open File to write the D3 Graph
    output_file = open('demo.html', 'w')

    type = 'pieChart'
    chart = pieChart(name=type, color_category='category20c', height=450, width=450)
    chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")

    xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
    ydata = [3, 4, 0, 1, 5, 7, 3]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildhtml()
    output_file.write(chart.htmlcontent)

    # close Html file
    output_file.close()


@app.route("/test")
def create_chart():
    # Open File to write the D3 Graph
    output_file = open('output.html', 'w')

    type = 'pieChart'
    chart = pieChart(name=type, color_category='category20c', height=450, width=450)
    chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")

    x = []
    xdata = []
    ydata = []
    user_language = session.query(Tweet.user_lang)
    d = defaultdict(int)
    for language in user_language:
        d[language] += 1
    language = list(d.keys())
    new_list = []
    for item in language:
        new_list.append(item[0])
    count = list(d.values())
    xdata = new_list
    ydata = count

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildhtml()
    output_file.write(chart.htmlcontent)

    # close Html file
    output_file.close()
    return render_template("test-nvd3.html")

@app.route("/user_lang")
def user_language():
    return render_template("user_lang.html")

@app.route("/user_language_api")
def user_language_api():
    user_language = session.query(Tweet.user_lang)
    user_language_test = []
    for i in user_language:
        user_language_test.append(i[0])
    d = Counter(user_language_test)
    chart_values = [{"value": value, "label": key} for key, value in d.items()]
    data = [{"values": chart_values, "key": "Series 1"}]
    return Response(json.dumps(data), 201, mimetype="application/json")
    
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

@app.route("/created_at_day_api")
def created_at_day_api():
    x = []
    x2 = []
    day_clean = []
    month_clean = []
    month_date_clean = []
    year_clean = []
    created_at = session.query(Tweet.created_at)
    for i in created_at:
        x.append(i)
    for i in created_at:
        x2.append(i[0])
    for i in x2:
        day_clean.append(datetime.datetime.strptime(i, "%a  %b %d %H:%M:%S %z %Y").day)
    #count them up
    day_counter = Counter(day_clean)
    #month_counter = Counter(month_clean)
    #month_date_counter = Counter(month_date_clean)
    #year_counter = Counter(year_clean)
    #build the chart values for day
    chart_values_day = [{"y": value, "x": key} for key, value in day_counter.items()]
    chart_values_day.sort(key=lambda i: i["x"])
    print(chart_values_day)
    data = [{"yAxis": "1","values": chart_values_day, "key": "Day of the Week"}]
    #build the chart values for month
    #chart_values_month = [{"y": value, "x": key} for key, value in month_counter.items()]
    #full_chart_values_month = [{"yAxis": "1","values": chart_values_month, "key": "Month"}]
    #build the chart values for month and date
    #chart_values_month_date = [{"y": value, "x": key} for key, value in month_date_counter.items()]
    #full_chart_values_month_date = [{"yAxis": "1","values": chart_values_month_date, "key": "Date"}]
    #build the chart values for year
    #chart_values_year = [{"y": value, "x": key} for key, value in year_counter.items()]
    #full_chart_values_year = [{"yAxis": "1","values": chart_values_year, "key": "Year"}]
    return Response(json.dumps(data), 201, mimetype="application/json")

@app.route("/created_at_month_api")
def created_at_month_api():
    x = []
    x2 = []
    #day_clean = []
    month_clean = []
    #month_date_clean = []
    #year_clean = []
    created_at = session.query(Tweet.created_at)
    for i in created_at:
        x.append(i)
    for i in created_at:
        x2.append(i[0])
    # break out the individual time unites
    for i in x2:
        month_clean.append(datetime.datetime.strptime(i, "%a  %b %d %H:%M:%S %z %Y").month)
        #day_clean.append(i[:3])
        #month_clean.append(i[4:7])
        #month_date_clean.append(i[4:10])
        #year_clean.append(i[26:30])
    #count them up
    #day_counter = Counter(day_clean)
    month_counter = Counter(month_clean)
    #month_date_counter = Counter(month_date_clean)
    #year_counter = Counter(year_clean)
    #build the chart values for day
    #chart_values_day = [{"y": value, "x": key} for key, value in day_counter.items()]
    #data = [{"yAxis": "1","values": chart_values_day, "key": "Day of the Week"}]
    #build the chart values for month
    chart_values_month = [{"y": value, "x": key} for key, value in month_counter.items()]
    chart_values_month.sort(key=lambda i: i["x"])
    print(chart_values_month)
    data = [{"yAxis": "1","values": chart_values_month, "key": "Month"}]
    #build the chart values for month and date
    #chart_values_month_date = [{"y": value, "x": key} for key, value in month_date_counter.items()]
    #full_chart_values_month_date = [{"yAxis": "1","values": chart_values_month_date, "key": "Date"}]
    #build the chart values for year
    #chart_values_year = [{"y": value, "x": key} for key, value in year_counter.items()]
    #full_chart_values_year = [{"yAxis": "1","values": chart_values_year, "key": "Year"}]
    return Response(json.dumps(data), 201, mimetype="application/json")
    
@app.route("/created_at_year_api")
def created_at_year_api():
    x = []
    x2 = []
    #day_clean = []
    #month_clean = []
    #month_date_clean = []
    year_clean = []
    created_at = session.query(Tweet.created_at)
    for i in created_at:
        x.append(i)
    for i in created_at:
        x2.append(i[0])
    # break out the individual time unites
    for i in x2:
        year_clean.append(datetime.datetime.strptime(i, "%a  %b %d %H:%M:%S %z %Y").year)
        #day_clean.append(i[:3])
        #month_clean.append(i[4:7])
        #month_date_clean.append(i[4:10])
        #year_clean.append(i[26:30])
    #count them up
    #day_counter = Counter(day_clean)
    #month_counter = Counter(month_clean)
    #month_date_counter = Counter(month_date_clean)
    year_counter = Counter(year_clean)
    #build the chart values for day
    #chart_values_day = [{"y": value, "x": key} for key, value in day_counter.items()]
    #data = [{"yAxis": "1","values": chart_values_day, "key": "Day of the Week"}]
    #build the chart values for month
    #chart_values_month = [{"y": value, "x": key} for key, value in month_counter.items()]
    #data = [{"yAxis": "1","values": chart_values_month, "key": "Month"}]
    #build the chart values for month and date
    #chart_values_month_date = [{"y": value, "x": key} for key, value in month_date_counter.items()]
    #full_chart_values_month_date = [{"yAxis": "1","values": chart_values_month_date, "key": "Date"}]
    #build the chart values for year
    chart_values_year = [{"y": value, "x": key} for key, value in year_counter.items()]
    chart_values_year.sort(key=lambda i: i["x"])
    print(chart_values_year)
    data = [{"yAxis": "1","values": chart_values_year, "key": "Year"}]
    return Response(json.dumps(data), 201, mimetype="application/json")
    
@app.route("/created_at")
def created_at():
    return render_template("created_at.html")

@app.route("/favorite_count")
def favorite_count():
    x = []
    favorite_count = session.query(Tweet.favorite_count)
    for i in favorite_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("favorite_count.html", json_data=json_data)

@app.route("/tweet_language_api")
def tweet_language_api():
    tweet_language = session.query(Tweet.tweet_lang)
    tweet_language_test = []
    for i in tweet_language:
        tweet_language_test.append(i[0])
    d = Counter(tweet_language_test)
    chart_values = [{"value": value, "label": key} for key, value in d.items()]
    data = [{"values": chart_values, "key": "Series 1"}]
    return Response(json.dumps(data), 201, mimetype="application/json")

@app.route("/tweet_lang")
def tweet_language():
    return render_template("tweet_lang.html")

@app.route("/retweet_count")
def retweet_count():
    x = []
    retweet_count = session.query(Tweet.retweet_count)
    for i in retweet_count:
        x.append(i)
    json_data = json.dumps(x)
    return render_template("retweet_count.html", json_data=json_data)

@app.route("/filter")
def filter():
    x = []
    tweet_language_test = []
    user_language_test = []
    favorite_count_test = []
    text = session.query(Tweet.text).order_by(Tweet.id).all()
    tweet_language = session.query(Tweet.tweet_lang).order_by(Tweet.id).all()
    user_language = session.query(Tweet.user_lang).order_by(Tweet.id).all()
    favorite_count = session.query(Tweet.favorite_count).order_by(Tweet.id).all()
    for i in text:
        x.append(i[0])
    for i in tweet_language:
        tweet_language_test.append(i[0])
    for i in user_language:
        user_language_test.append(i[0])
    for i in favorite_count:
        favorite_count_test.append(i[0])
    return render_template("filter.html", values=zip(x, tweet_language_test, user_language_test, favorite_count_test))

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

