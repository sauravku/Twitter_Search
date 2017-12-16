#!/usr/bin/env python

import twitter
import json
import datetime
import pycountry

"""
twitter-search

* API to query data from Twitter based on search term
* Data must be filterable based on any key in the search data.
* User should be able to search fields inside Array as well in the stored data.
* Complex filters dependent on data-type needs to be implemented. For example,
* Date range filter in case of date
   * Less than, greater than, equal to filter in case of integer
   * Starts with, ends with, contains, exact match in case of string
* Implement sort option
* Implement group by option
* API to export data based on filters
"""

class Tweet(object):
        def __init__(self, query):
                self.retweet_count = int ( query["retweet_count"] )
                self.id_ = int( query["id"] )
                self.text = query["text"].encode('utf-8')
                self.user = query["user"]["screen_name"].encode('utf-8')
                # time in utc format
                date = query["created_at"].encode()
                self.created_at = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
                language = query["lang"].encode()
                try:
                        self.lang = pycountry.languages.get(alpha_2=language).name
                except:
                        self.lang = None
                try:
                        self.place = query["place"]["name"].encode()
                        self.country = query["place"]["country"].encode()
                except:
                        self.place = None
                        self.country = None
                        
                
        def __repr__(self):
                return "%s %s (%s) %s %s %s" % ( self.id_, self.retweet_count,
                                                 self.created_at, self.lang,
                                                 self.place, self.country)

class Search(object):
        def __init__(self):
                config = {}
                execfile("config.py", config)
                self.twitter = twitter.Twitter(auth = twitter.OAuth(config["access_key"],
                                                                    config["access_secret"],
                                                                    config["consumer_key"],
                                                                    config["consumer_secret"]))
                self.tweet = []

        # query twitter for searching tweets
        def searchTweets(self, search_term, count=15, until=None):
                self.search_term = search_term
                self.count = count
                # TODO: set until to None result in known exception
                if not until:
                        until = (datetime.datetime.utcnow().date() + \
                                 datetime.timedelta(days=1)).strftime("%Y-%m-%d")  
                # Returns tweets created before the given date.
                # Date should be formatted as YYYY-MM-DD.
                # No tweets will be found for a date older than one week.
                self.until = until
                self.query = self.twitter.search.tweets(q=self.search_term,
                                                        count=self.count,until=self.until)
                self.generateTweets()

        # return search time
        def completeSearchTime(self):
                return self.query["search_metadata"]["completed_in"]

        # generate per tweet object
        def generateTweets(self):
                for t in self.query["statuses"]:
                        self.tweet.append( Tweet(t) )

        def sortByDate(self):
                self.tweet.sort(key=lambda tup: tup.created_at, reverse=True)
                
search = Search()
search.searchTweets("trump", count=100)

search.sortByDate()
print "Search complete (%.3f seconds)" % search.completeSearchTime()

for tweet in search.tweet:        
        print tweet

