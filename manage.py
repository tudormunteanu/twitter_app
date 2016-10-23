import os
from flask.ext.script import Manager

from twitter_app import app
from twitter_app.twitter_streaming import Main, get_tweets

from redis import Redis
from rq import Queue
from rq.job import Job

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def tweepy_worker():
    #os.system("sudo service redis-server start")
    #os.system("rq worker")
    q = Queue(connection=Redis())
    tweet_number = input("How many tweets do you want?")
    # maybe do this as sys arg?
    try:
        number = int(tweet_number)
    except ValueError:
        print("Please enter a valid number")
    result = q.enqueue(get_tweets, result_ttl=5000, number=number)
    print(result)
    
if __name__ == "__main__":
    manager.run()
    