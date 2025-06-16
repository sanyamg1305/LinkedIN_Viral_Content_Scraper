import requests
from datetime import datetime, timedelta
import re

SERPAPI_API_KEY = "3b30912828c65641526f3dce1f3e0865fde81c7d59950524ac565bf2ab5ddbdd"

def extract_post_id(linkedin_url):
    # Extract the post ID from LinkedIn URL
    pattern = r"posts/([^/]+)"
    match = re.search(pattern, linkedin_url)
    if match:
        return match.group(1)
    print(f"Could not extract post ID from URL: {linkedin_url}")
    return None

def fetch_linkedin_posts(topics):
    print(f"Starting to fetch LinkedIn posts for topics: {topics}")
    results = []
    date_range = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    for topic in topics:
        print(f"\nProcessing topic: {topic}")
        search_queries = [
            f"site:linkedin.com/posts {topic} engagement",
            f"site:linkedin.com/posts {topic} viral",
            f"site:linkedin.com/posts {topic} trending"
        ]

        for query in search_queries:
            print(f"\nExecuting search query: {query}")
            params = {
                "engine": "google",
                "q": query,
                "hl": "en",
                "gl": "us",
                "api_key": SERPAPI_API_KEY,
                "num": 15,  # Increased to 15 results per query
                "as_qdr": "m1"
            }

            try:
                print("Making request to SerpAPI...")
                response = requests.get("https://serpapi.com/search", params=params)
                data = response.json()
                print(f"Received response from SerpAPI. Status code: {response.status_code}")
                
                if "error" in data:
                    print(f"SerpAPI returned an error: {data['error']}")
                    continue
                    
                top_results = data.get("organic_results", [])[:15]
                print(f"Found {len(top_results)} results for query")

                for result in top_results:
                    post_id = extract_post_id(result.get("link", ""))
                    results.append({
                        "topic": topic,
                        "title": result.get("title", "No title"),
                        "link": result.get("link", "No link"),
                        "snippet": result.get("snippet", "No snippet"),
                        "post_id": post_id
                    })

            except Exception as e:
                print(f"Error fetching results for query '{query}': {str(e)}")
                continue

    # Remove duplicates based on link
    seen_links = set()
    unique_results = []
    for result in results:
        if result["link"] not in seen_links:
            seen_links.add(result["link"])
            unique_results.append(result)

    print(f"\nFinal results count: {len(unique_results)}")
    return unique_results[:15]