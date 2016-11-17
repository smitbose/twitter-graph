import tweepy


def start_auth():


    consumer_key = 'NHSZRHkxsxKl8KEcXmtlSz0Q4'# input("Enter the consumer key")
    consumer_secret = 'Wj3HfdUHgz6iI2dN4rQw5qKxOFzPur45l6fQiA83ymg07Kb9vr' # input("Enter the consumer secret")
    access_token = '221692856-AAawq2zFH1hQRNIw5s39NKo21g671JXwldwZqZ3y' # input("Enter the access_token")
    access_token_secret = 'KNQ1wapBNU2KXMHhorKyzxYckPzNHiSlqaJ6ztoha1SCO' # input("Enter the access token secret")


    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)

    return api