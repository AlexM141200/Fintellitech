import requests
import pandas as pd
from textblob import TextBlob
import sys

# Define the list of companies you are interested in
company = sys.argv[1]

# Search for comments on Reddit that mention the companies
comments = []
print(f"Searching for comments about {company}...")
response = requests.get(f"https://api.pushshift.io/reddit/comment/search/?subreddit=technology&q={company}&size=100")
comments += [comment["body"] for comment in response.json()["data"]]

# Save the comments to a CSV file
comments_df = pd.DataFrame({'comment': comments})
comments_df.to_csv('comments.csv', index=False)

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

# Load the comments from the CSV file and apply the sentiment analysis function
comments_df = pd.read_csv('comments.csv')
comments_df['sentiment'] = comments_df['comment'].apply(get_comment_sentiment)

# Calculate the percentage of comments that are positive, negative, and neutral
sentiment_counts = comments_df['sentiment'].value_counts(normalize=True)
positive_percent = sentiment_counts['positive'] * 100
negative_percent = sentiment_counts['negative'] * 100
neutral_percent = sentiment_counts['neutral'] * 100

# Print the results
print('Public sentiment about the companies:')
print(f'Positive: {positive_percent:.1f}%')
print(f'Negative: {negative_percent:.1f}%')
print(f'Neutral: {neutral_percent:.1f}%')
