import feedparser
import requests
import os

def fetch_rss_feed(feed_url):
    """Reads the RSS feed and returns the first entry."""
    feed = feedparser.parse(feed_url)
    if len(feed.entries) > 0:
        first_entry = feed.entries[0]
        return {
            "title": first_entry.title,
            "link": first_entry.link,
            "description": first_entry.description
        }
    return None

def linkedin_post(title, link, description):
    """Posts to LinkedIn using the UGC Posts API."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    org_id = os.getenv("LINKEDIN_ORG_ID")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "author": f"urn:li:organization:104661399",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"{title}\n\n{description}\n\nRead more: {link}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", 
        headers=headers, 
        json=post_data
    )

    if response.status_code == 201:
        print("Post successful!")
    else:
        print(f"Error posting to LinkedIn: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    # RSS feed URL
    feed_url = "https://claromes.com/feeds/rss.xml"
    
    # Fetch RSS feed
    rss_item = fetch_rss_feed(feed_url)
    
    if rss_item:
        # Post to LinkedIn
        linkedin_post(rss_item["title"], rss_item["link"], rss_item["description"])
    else:
        print("No items found in the RSS feed.")
