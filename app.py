import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
 
# Replace with your real Bearer Token from Twitter Developer Portal
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}
 
def get_user_info(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = create_headers()
    params = {
        "user.fields": "description,location,created_at,public_metrics"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None
    return response.json()['data']
 
def get_user_tweets(user_id, max_results=10):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = create_headers()
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []
    return response.json().get('data', [])

def summarize_tweets(user_info, tweets):
    content = f"""Twitter Profile:
    Name: {user_info['name']}
    Bio: {user_info['description']}
    Location: {user_info.get('location','Not Provided')}
    Followers: {user_info['public_metrics']['followers_count']}
    Recent Tweets:
    """
    for tweet in tweets:
        content += f"- {tweet['text']}\n"

    system_prompt = f"""
    You are a sales assistant. Analyze the following Twitter profile and recent tweets of a person.
    Your task is to:
    Summarize the person’s interests and topics they frequently tweet about.
    Identify any patterns related to their likes or dislikes.
    Translate any non-English tweets to English before analyzing.

    Return clear, concise bullet points highlighting:
    -> Personality traits (if any can be inferred)
    -> Topics they care about or follow often
    -> Hobbies, products, or industries they mention or interact with
    -> Anything that could help a salesperson build rapport or context
    -> Also give two potential icebreakers
    Keep the tone professional and neutral. Use 5–7 bullet points.

    Here is the content:
    {content}
    """

    response = model.generate_content(system_prompt)
    return response.text

def main():
    username = input("Enter Twitter username (without @): ")
    user_info = get_user_info(username)
 
    if user_info:
        print("\n👤 User Info")
        print("-----------")
        print(f"Name      : {user_info['name']}")
        print(f"Username  : @{user_info['username']}")
        print(f"Bio       : {user_info['description']}")
        print(f"Location  : {user_info.get('location', 'Not Provided')}")
        print(f"Followers : {user_info['public_metrics']['followers_count']}")
        # print(f"Joined    : {user_info['created_at']}")
 
        tweets = get_user_tweets(user_info['id'])
 
        print("\n📝 Recent Tweets")
        print("----------------")
        if tweets:
            for tweet in tweets:
                print(f"{tweet['created_at']}: {tweet['text']}\n")
        else:
            print("No recent tweets found.")
        
        print("\n🧠 Gemini Summary")
        print("-----------------")
        summary = summarize_tweets(user_info, tweets)
        print(summary)
 
if __name__ == "__main__":
    main()