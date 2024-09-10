import feedparser
import requests
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def html_parser(text):
    """Removes HTML tags from a string."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def id_parser(text):
    """Extracts text between the second ':' and '/' and adds a space before the second uppercase letter."""
    # Regex to capture text between the second ':' and '/'
    match = re.search(r':[^:]+:([^/]+)/', text)
    if match:
        extracted_text = match.group(1)
        # Regex to add space before the second uppercase letter
        processed_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', extracted_text, 1)
        return processed_text
    return None

def date_parser(date_str):
    """Formats the date string to 'Month Day, Year'."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.strftime('%B %d, %Y')

def fetch_blog(feed_url):
    """Reads the feed and returns the first entry."""
    feed = feedparser.parse(feed_url)
    if len(feed.entries) > 0:
        first_entry = feed.entries[0]
        return {
            "title": html_parser(first_entry.title),
            "description": html_parser(first_entry.description),
            "link": first_entry.link
        }
    return None

def fetch_github(feed_url):
    """Reads the feed and returns the first entry."""
    feed = feedparser.parse(feed_url)
    entries = []
    if len(feed.entries) >= 5:
        for entry in feed.entries[:5]:
            entries.append({
                "id": id_parser(entry.id),
                "title": f'@{entry.title}',
                "link": entry.link,
                "date": date_parser(entry.published)
            })
    return entries

def format_blog_posts(entry):
    """Formats the last blog entry for posting."""
    formatted_post = f"{entry['title']}\n\n{entry['description']}\n\nRead more: {entry['link']}\n\nThis is an automatic post."
    return formatted_post

def format_github_posts(entries):
    """Formats the last 5 GitHub entries for posting."""
    formatted_posts = ""
    for i, github_item in enumerate(entries, start=1):
        formatted_posts += f"{i}. {github_item['title']} · {github_item['date']}\n\n{github_item['id']}: {github_item['link']}\n\nThis is an automatic post.\n\n"
    return formatted_posts

def linkedin_post(item_post):
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
                    "text": f"{item_post}"
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
    # Feeds URL
    blog = "https://claromes.com/feeds/rss.xml"
    github = "https://github.com/claromes.atom"

    # Fetch and format feeds
    blog_item = fetch_blog(blog)
    blog_item_post = format_blog_posts(blog_item)

    github_item = fetch_github(github)
    github_item_post = format_github_posts(github_item)

    # Post to LinkedIn
    if blog_item:
        linkedin_post(blog_item_post)

    if github_item:
        linkedin_post(github_item_post)
