import requests
import pandas as pd
from textblob import TextBlob


def get_public_perception(company):
    comments = []
    print(f"Searching for comments about {company}...")
    response = requests.get(
        f"https://api.pushshift.io/reddit/comment/search/?subreddit=technology&q={company}&size=100")
    comments += [comment["body"] for comment in response.json()["data"]]

    comments_df = pd.DataFrame({'comment': comments})

    def get_comment_sentiment(comment):
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0.2:
            return "positive"
        elif sentiment_score < -0.2:
            return "negative"
        else:
            return "neutral"

    comments_df['sentiment'] = comments_df['comment'].apply(
        get_comment_sentiment)

    sentiment_counts = comments_df['sentiment'].value_counts(normalize=True)
    positive_percent = sentiment_counts['positive'] * 100
    negative_percent = sentiment_counts['negative'] * 100
    neutral_percent = sentiment_counts['neutral'] * 100

    analysis = f"Public sentiment about {company}:\nPositive: {positive_percent:.1f}%\nNegative: {negative_percent:.1f}%\nNeutral: {neutral_percent:.1f}%."
    return analysis
