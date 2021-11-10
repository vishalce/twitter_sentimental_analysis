import re

from textblob import TextBlob
from tweepy import OAuthHandler, API, TweepyException, TwitterServerError


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'CONSUMER_KEY'
        consumer_secret = 'CONSUMER_SECRET'
        access_token = 'ACCESS_TOKEN'
        access_token_secret = 'ACCESS_TOKEN_SECRET'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(
                consumer_key=consumer_key, consumer_secret=consumer_secret
            )
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = API(self.auth)
        except TweepyException as ex:
            print(f'Error: Authentication Failed with exception: {ex}')

    def clean_tweet(self, tweet):
        """
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(
            re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)', ' ', tweet).split()
        )

    def get_tweet_sentiment(self, tweet):
        """
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        return 'positive' \
            if analysis.sentiment.polarity > 0 \
            else 'neutral' if analysis.sentiment.polarity == 0 \
            else 'negative'

    def get_tweets(self, query, count=10000):
        """
        Main function to fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, lang="en", count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # saving sentiment of tweet
                parsed_tweet = {
                    'tweet': tweet.text,
                    'sentiment': self.get_tweet_sentiment(tweet.text),
                }
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except TwitterServerError as err:
            # print error (if any)
            print(f'Error : {str(err)}')
