import os
import tweepy
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Check if all required variables are loaded
def check_env_vars():
    if not all([TWITTER_API_KEY, TWITTER_BEARER_TOKEN, TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, NEWS_API_KEY,
                EMAIL_USER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        raise EnvironmentError("One or more environment variables are missing.")

check_env_vars()

# Initialize Tweepy Client
client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
)

def fetch_latest_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print("News fetched successfully.")
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def load_posted_tweets():
    if os.path.exists("posted_tweets.txt"):
        try:
            with open("posted_tweets.txt", "r", encoding='utf-8') as file:
                return set(line.strip() for line in file)
        except UnicodeDecodeError:
            print("Error decoding posted_tweets.txt. File may contain non-UTF-8 characters.")
            return set()
    return set()

def save_posted_tweet(tweet):
    with open("posted_tweets.txt", "a", encoding='utf-8') as file:
        file.write(tweet + "\n")

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def tweet_news():
    articles = fetch_latest_news()
    if not articles:
        print("No articles to tweet.")
        return
    
    posted_tweets = load_posted_tweets()
    
    for article in articles[:5]:  # Tweeting the top 5 articles
        title = article['title']
        if len(title) > 280:
            title = title[:277] + "..."
        if title in posted_tweets:
            print(f"Skipping duplicate tweet: {title}")
            continue
        try:
            client.create_tweet(text=title)
            save_posted_tweet(title)
            print(f"Successfully tweeted: {title}")
            send_email("Twitter Bot Status", f"Successfully tweeted: {title}")
        except tweepy.TooManyRequests as e:
            print(f"Rate limit error: {e}")
            send_email("Twitter Bot Error", f"Rate limit error: {e}")
            time.sleep(15 * 60)  # Sleep for 15 minutes
        except tweepy.TweepyException as e:
            print(f"Error tweeting: {e}")
            send_email("Twitter Bot Error", f"Error tweeting: {e}")

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Script started at: {start_time}")
    
    while True:
        tweet_news()
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        print(f"Current time: {current_time}, Elapsed time: {elapsed_time}")
        time.sleep(3600)  # Sleep for 1 hour before fetching and tweeting news again
