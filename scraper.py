import requests
from datetime import datetime, timedelta

SERPAPI_API_KEY = "3b30912828c65641526f3dce1f3e0865fde81c7d59950524ac565bf2ab5ddbdd"

def fetch_linkedin_posts(topics):
    results = []
    # Get posts from the last 30 days for better engagement
    date_range = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    for topic in topics:
        # Enhanced search query to find more engaging content
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
                "num": 15,  # Increased to 15 results
                "as_qdr": "m1"  # Last month
            }

            try:
                response = requests.get("https://serpapi.com/search", params=params)
                data = response.json()

                top_results = data.get("organic_results", [])[:15]

                for result in top_results:
                    # Extract engagement metrics from the snippet if available
                    snippet = result.get("snippet", "")
                    engagement_metrics = {
                        "likes": 0,
                        "comments": 0,
                        "shares": 0
                    }

                    # Try to parse engagement numbers from the snippet
                    if "likes" in snippet.lower():
                        try:
                            likes_text = snippet.lower().split("likes")[0].split()[-1]
                            engagement_metrics["likes"] = int(likes_text.replace(",", ""))
                        except:
                            pass

                    if "comments" in snippet.lower():
                        try:
                            comments_text = snippet.lower().split("comments")[0].split()[-1]
                            engagement_metrics["comments"] = int(comments_text.replace(",", ""))
                        except:
                            pass

                    if "shares" in snippet.lower():
                        try:
                            shares_text = snippet.lower().split("shares")[0].split()[-1]
                            engagement_metrics["shares"] = int(shares_text.replace(",", ""))
                        except:
                            pass

                    results.append({
                        "topic": topic,
                        "title": result.get("title", "No title"),
                        "link": result.get("link", "No link"),
                        "snippet": snippet,
                        "engagement": engagement_metrics,
                        "total_engagement": sum(engagement_metrics.values())
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

    return unique_results[:15]  # Return top 15 most engaging unique posts