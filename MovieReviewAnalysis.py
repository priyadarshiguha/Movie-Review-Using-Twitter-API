# Importing required libraries
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plot

# Twitter Api credentials...
consumer_key = 'HGAY9bOci1I38ReJNwwc0zvMS'
consumer_secret_key = 'iAqQISRjwFeQIRBuXxJL1qWF9j1WDQBfhBGtBCyRK7hJTGWS4p'
access_token = '1613023332-vqsPFI5wTJUKfB2p8LfrUnny6HEuEzFl9EqNnej'
access_token_secret = 'vJ6nkvyTn7w1RHFzYduWhwKJ1AqMFvZkFtDUHyR1Fh0a7'

# Connecting to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# User Input
# Number of tweets to be analyzed and the movie #hashtag
count = int(input("Enter The Number Of Tweets You Want To Analyze: "))
movie = input("Enter Movie Name: ")

# Retrieving tweets
# search() can return only 100 tweets at a time
temp = 0
last_tweet_id = ""
public_tweets = {}

while temp < count:
    if temp == 0:
        if count <= 100:
            temp_tweets = api.search(movie, count=count, tweet_mode="extended")
            for i in temp_tweets:
                public_tweets[i.id_str] = i.full_text
            temp += count
            last_tweet_id = min(public_tweets.keys())
        elif count > 100:
            temp_tweets = api.search(movie, count=100, tweet_mode="extended")
            for i in temp_tweets:
                public_tweets[i.id_str] = i.full_text
            temp += 100
            last_tweet_id = min(public_tweets.keys())
    elif temp > 0:
        if count > 100 and count - temp > 100:
            temp_tweets = api.search(movie, count=100, tweet_mode="extended", max_id=last_tweet_id)
            for i in temp_tweets:
                public_tweets[i.id_str] = i.full_text
            temp += 100
            last_tweet_id = min(public_tweets.keys())
        elif count - temp <= 100:
            temp_tweets = api.search(movie, count=count - temp, tweet_mode="extended", max_id=last_tweet_id)
            for i in temp_tweets:
                public_tweets[i.id_str] = i.full_text
            temp += 100
            last_tweet_id = min(public_tweets.keys())

# Cleaning the tweets to discard any special characters.
tweet_dict = {}
i = 1

for tweet in public_tweets:
    tweet_dict[tweet] = public_tweets[tweet]
    tweet_dict[tweet] = ''.join(c for c in tweet_dict[tweet] if c <= '\uFFFF')
    i = i + 1

# Analyzing and categorizing tweets
tweet_analysis = {}
for tweet in tweet_dict:
    analysis = TextBlob(tweet_dict[tweet])
    if analysis.sentiment.polarity > 0:
        tweet_analysis[tweet] = 'positive'
    elif analysis.sentiment.polarity == 0:
        tweet_analysis[tweet] = 'neutral'
    else:
        tweet_analysis[tweet] = 'negative'

# Representing the final result in the form of a pie chart
count_positive = 0
count_negative = 0
count_neutral = 0

for i in tweet_analysis:
    if tweet_analysis[i] == 'positive':
        count_positive += 1
    elif tweet_analysis[i] == 'neutral':
        count_neutral += 1
    else:
        count_negative += 1

pie_label = ['Positive', 'Negative', 'Neutral']
pie_data = [count_positive, count_negative, count_neutral]

fig, ax = plot.subplots()
ax.pie(pie_data, labels=pie_label, colors=['green', 'red', 'yellow'])
ax.axis('equal')
plot.title(movie)
plot.show()

# END
