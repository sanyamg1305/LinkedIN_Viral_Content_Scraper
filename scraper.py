import requests

SERPAPI_API_KEY = "3b30912828c65641526f3dce1f3e0865fde81c7d59950524ac565bf2ab5ddbdd"

def fetch_linkedin_posts(topics):
    results = []

    for topic in topics:
        params = {
            "engine": "google",
            "q": f"site:linkedin.com/posts {topic}",
            "hl": "en",
            "gl": "us",
            "api_key": SERPAPI_API_KEY
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        top_results = data.get("organic_results", [])[:10]

        for result in top_results:
            results.append({
                "topic": topic,
                "title": result.get("title", "No title"),
                "link": result.get("link", "No link"),
                "snippet": result.get("snippet", "No snippet")
            })

    return results
