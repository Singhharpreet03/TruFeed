import requests
from requests_oauthlib import OAuth1
import json

def append_to_file(text_block, file_name='tweets.txt'):
    """
    Append the given text_block to file_name.
    Creates the file if it does not exist.
    """
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(text_block)
        f.write('\n')  

def fetch_latest_tweets(consumer_key, consumer_secret, access_token, access_token_secret):
    # Define the API endpoint
    # url = "https://api.twitter.com/2/tweets/search/recent?query=%23Ai%20-is:retweet%20has:media&expansions=attachments.media_keys,author_id&tweet.fields=created_at,author_id,public_metrics,attachments&media.fields=media_key,type,url,preview_image_url,height,width,public_metrics&max_results=10"
    
    url = (
    "https://api.twitter.com/2/tweets/search/recent"
    "?query=%23Ai%20-is%3Aretweet%20has%3Amedia"
    "&expansions=attachments.media_keys,author_id"
    "&tweet.fields=created_at,author_id,public_metrics,attachments"
    "&media.fields=media_key,type,url,preview_image_url,height,width,public_metrics"
    "&max_results=10"
)
    # Set up OAuth 1.0a authentication
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    
    try:
        # Make the API request
        response = requests.get(url, auth=auth)
        
        # Print request headers for debugging
        print("Request Headers:", response.request.headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract tweets and related data
        tweets = data.get('data', [])
        includes = data.get('includes', {})
        users = {user['id']: user for user in includes.get('users', [])}
        media = {media['media_key']: media for media in includes.get('media', [])}
        
        # Process and print the tweets
        for tweet in tweets:
            author = users.get(tweet['author_id'], {})
            attachments = tweet.get('attachments', {})
            media_keys = attachments.get('media_keys', [])
            
            print(f"Tweet ID: {tweet['id']}")
            print(f"Created at: {tweet['created_at']}")
            print(f"Author: {author.get('username', 'Unknown')}")
            print(f"Text: {tweet['text']}")
            
            # Display media information
            for media_key in media_keys:
                media_item = media.get(media_key, {})
                print(f"Media Type: {media_item.get('type')}")
                if media_item.get('url'):
                    print(f"Media URL: {media_item.get('url')}")
                if media_item.get('preview_image_url'):
                    print(f"Preview Image URL: {media_item.get('preview_image_url')}")
            
            # Display public metrics
            metrics = tweet.get('public_metrics', {})
            print(f"Likes: {metrics.get('like_count', 0)}")
            print(f"Retweets: {metrics.get('retweet_count', 0)}")
            print(f"Replies: {metrics.get('reply_count', 0)}")
            print("-" * 50)
        
        return tweets
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tweets: {e}")
        print("Response Content:", e.response.text if e.response else "No response content")
        return []

if __name__ == "__main__":
    # Replace these with your actual Twitter API credentials
    # CONSUMER_KEY = "your_consumer_key"
    # CONSUMER_SECRET = "your_consumer_secret"
    # ACCESS_TOKEN = "your_access_token"
    # ACCESS_TOKEN_SECRET = "your_access_token_secret"
    
    # fetch_latest_tweets(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


    # # Replace these with your actual Twitter API credentials
    CONSUMER_KEY = "SAs4myIEMB4kzqZV7AmhjenAD"
    CONSUMER_SECRET = "WbXQlCYR8Mv6PWYJDCyAD1nUkOu54zH0llslFPA4GpPz8oKBiE"
    ACCESS_TOKEN = "1946848951317221376-mJV1sm0NisbiSBhU861dxNf0DvNE2y"
    ACCESS_TOKEN_SECRET = "8pbvuucdZwwgAQtdnX7j0vOz8Ujbt8UW9FjNlTEQmtd1n"
    
    fetch_latest_tweets(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)