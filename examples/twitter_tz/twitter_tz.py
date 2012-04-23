#!/usr/bin/env python
# encoding: utf-8

'''
File: twitter_tz.py
Author: AFlock
Description: Given a database of tweets, aggregate number of tweets per timezone
Note: before running this job fill a mongodb with tweets by running :
curl https://stream.twitter.com/1/statuses/sample.json -u<user>:<pass> | mongoimport -c twitter


'''

from disco.core        import Job, result_iterator
from mongodb_io        import mongodb_input_stream
from app.MongoSplitter import calculate_splits

config = {
        "inputURI":"mongodb://localhost/twitter",
        "createInputSplits" : True,
        }

def map(tweet, params):
    yield tweet['user'].get('time_zone', "unlisted"), 1

def reduce(iter, params):
    from disco.util import kvgroup
    for zone, number in kvgroup(sorted(iter)):
        yield zone, sum(number)

if __name__ == '__main__':
    job = Job().run(input=calculate_splits(config) ,
            map = map,
            reduce = reduce,
            map_input_stream = mongodb_input_stream
            )

    for tz, count in result_iterator(job.wait(show=True)):
        print "TZ : %s :: Count : %s" % (tz, count)
