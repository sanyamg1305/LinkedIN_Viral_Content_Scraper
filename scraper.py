import requests
from datetime import datetime, timedelta
from linkedin_api import Linkedin
import re

SERPAPI_API_KEY = "3b30912828c65641526f3dce1f3e0865fde81c7d59950524ac565bf2ab5ddbdd"
# LinkedIn credentials
LINKEDIN_EMAIL = "golechhasanyam2005@gmail.com"  # Replace with your dummy account email
LINKEDIN_PASSWORD = "Barcelona@1305"  # Replace with your dummy account password

def extract_post_id(linkedin_url):
    # Extract the post ID from LinkedIn URL
    pattern = r"posts/([^/]+)"
    match = re.search(pattern, linkedin_url)
    if match:
        return match.group(1)
    return None

def get_post_engagement(api, post_id):
    try:
        post_data = api.get_post(post_id)
        if post_data:
            return {
                "likes": post_data.get("numLikes", 0),
                "comments": post_data.get("numComments", 0),
                "shares": post_data.get("numShares", 0)
            }
    except Exception as e:
        print(f"Error fetching engagement for post {post_id}: {str(e)}")
    return {"likes": 0, "comments": 0, "shares": 0}

def fetch_linkedin_posts(topics):
    results = []
    date_range = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Initialize LinkedIn API
    try:
        api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    except Exception as e:
        print(f"Error initializing LinkedIn API: {str(e)}")
        return []

    for topic in topics:
        search_queries = [
            f"site:linkedin.com/posts {topic} engagement",
            f"site:linkedin.com/posts {topic} viral",
            f"site:linkedin.com/posts {topic} trending"
        ]

        for query in search_queries:
            params = {
                "engine": "google",
                "q": query,
                "hl": "en",
                "gl": "us",
                "api_key": SERPAPI_API_KEY,
                "num": 15,
                "as_qdr": "m1"
            }

            try:
                response = requests.get("https://serpapi.com/search", params=params)
                data = response.json()
                top_results = data.get("organic_results", [])[:15]

                for result in top_results:
                    post_id = extract_post_id(result.get("link", ""))
                    if post_id:
                        engagement = get_post_engagement(api, post_id)
                    else:
                        engagement = {"likes": 0, "comments": 0, "shares": 0}

                    results.append({
                        "topic": topic,
                        "title": result.get("title", "No title"),
                        "link": result.get("link", "No link"),
                        "snippet": result.get("snippet", "No snippet"),
                        "engagement": engagement,
                        "total_engagement": sum(engagement.values())
                    })

            except Exception as e:
                print(f"Error fetching results for query '{query}': {str(e)}")
                continue

    # Sort results by total engagement
    results.sort(key=lambda x: x["total_engagement"], reverse=True)
    
    # Remove duplicates based on link
    seen_links = set()
    unique_results = []
    for result in results:
        if result["link"] not in seen_links:
            seen_links.add(result["link"])
            unique_results.append(result)

    return unique_results[:15]