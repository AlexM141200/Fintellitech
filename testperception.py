import requests
import pandas as pd
from textblob import TextBlob


def get_public_perception(company):
    # Search for comments on Reddit that mention the company
    comments = []
    print(f"Searching for comments about {company}...")
    response = requests.get(
        f"https://api.pushshift.io/reddit/comment/search/?subreddit=technology&q={company}&size=100")
    comments += [comment["body"] for comment in response.json()["data"]]

    # Save the comments to a DataFrame
    comments_df = pd.DataFrame({'comment': comments})

    # Define the function to perform sentiment analysis on a single comment
    def get_comment_sentiment(comment):
        # Use TextBlob to perform sentiment analysis on the comment
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity

        # Classify the sentiment as positive, negative, or neutral based on the sentiment score
        if sentiment_score > 0.2:
            return "positive"
        elif sentiment_score < -0.2:
            return "negative"
        else:
            return "neutral"

    # Apply the sentiment analysis function to the comments DataFrame
    comments_df['sentiment'] = comments_df['comment'].apply(
        get_comment_sentiment)

    # Calculate the percentage of comments that are positive, negative, and neutral
    sentiment_counts = comments_df['sentiment'].value_counts(normalize=True)
    positive_percent = sentiment_counts['positive'] * 100
    negative_percent = sentiment_counts['negative'] * 100
    neutral_percent = sentiment_counts['neutral'] * 100

    # Construct and return the analysis response
    analysis = f"Public sentiment about {company}:\nPositive: {positive_percent:.1f}%\nNegative: {negative_percent:.1f}%\nNeutral: {neutral_percent:.1f}%"
    return analysis
