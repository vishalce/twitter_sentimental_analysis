import json

from bottle import route, run, hook, response, request

from twitter_client import TwitterClient


@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route('/api/sentimental-analysis/')
def sentimental():
    # creating object of TwitterClient Class
    hashtag = request.query['hashtag']
    api = TwitterClient()
    # calling function to get tweets

    people = {}

    tweets = api.get_tweets(query='#' + hashtag, count=10)

    # picking positive tweets from tweets
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    positive = 100 * len(positive_tweets) / len(tweets)
    # picking negative tweets from tweets
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    negative = 100 * len(negative_tweets) / len(tweets)
    # percentage of neutral tweets
    neutral = 100 * (len(tweets) - len(negative_tweets) - len(positive_tweets)) / len(tweets)
    data = {
        "parsed_tweets": len(tweets),
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "tweets": tweets,
    }
    response.content_type = 'application/json'
    return json.dumps(data)


run(host='0.0.0.0', port=8009, reloader=True)
