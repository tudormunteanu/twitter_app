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
    q = Queue(connection=Redis())
    result = q.enqueue(get_tweets, result_ttl=5000)
    print(result)
    
if __name__ == "__main__":
    manager.run()
    