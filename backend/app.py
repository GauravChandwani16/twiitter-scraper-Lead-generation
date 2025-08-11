import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
 
# Replace with your real Bearer Token from Twitter Developer Portal
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Create FastAPI app
app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body format
class AnalyzeRequest(BaseModel):
    username: str 
    company: str

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
 
def get_user_tweets(user_id, max_results=5):
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

def summarize_tweets(user_info, tweets, company_name):
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
    The person is associated with a company named "{company_name}".
    Your task is to:
    Summarize the person’s interests and topics they frequently tweet about.
    Identify any patterns related to their likes or dislikes.
    Translate any non-English tweets to English before analyzing.
    use the company name to infer any industry-specific interest, trends and insights

    **Instructions:**
    1. Summarize the person’s interests, topics they tweet about, and patterns in their likes/dislikes.
    2. Translate non-English tweets to English before analyzing.
    3. Use the company name to infer any industry-specific interests, trends, or insights.
    4. Keep tone professional and neutral.
    5. Return exactly 5–7 bullet points.
    6. **Output format must be ONLY bullet points starting with a dash ("-"), no extra headings, no arrows, no numbering.**
    7. Also give two potential icebreaker for sales person.

    Here is the content:
    {content}
    """

    response = model.generate_content(system_prompt)
    return response.text

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    user_info = get_user_info(request.username)
    if not user_info:
        raise HTTPException(status_code=404, details= "User not found")

    tweets = get_user_tweets(user_info['id'])
    summary = summarize_tweets(user_info, tweets, request.company)

    return {
        "user_info": user_info,
        "tweets": tweets,
        "summary": summary    
    }

@app.get("/")
def home():
    return {"message": "Backend is running!"}
