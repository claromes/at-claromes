import feedparser
import re
from datetime import datetime

from utils import load_posted_items, save_posted_items, is_item_posted, linkedin_post

def id_parser(text):
    """Extracts text between the second ':' and '/' and adds a space before the second uppercase letter."""
    match = re.search(r':[^:]+:([^/]+)/', text)
    if match:
        extracted_text = match.group(1)
        processed_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', extracted_text, 1)
        return processed_text
    return None

def date_parser(date_str):
    """Formats the date string to 'Month Day, Year'."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.strftime('%B %d, %Y')

def fetch_github(feed_url):
    """Reads the feed and returns the first 5 entries."""
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.entries[:5]:
        entries.append({
            "id": id_parser(entry.id),
            "title": f'@{entry.title}',
            "link": entry.link,
            "date": date_parser(entry.published)
        })
    return entries

def format_github_posts(entries):
    """Formats GitHub entries for posting."""
    formatted_posts_list = []
    for i, github_item in enumerate(entries, start=1):
        formatted_posts_list.append(f"{i}. {github_item['title']} · {github_item['date']}\n\n{github_item['id']}: {github_item['link']}")

    formatted_posts = "\n\n".join(formatted_posts_list)
    formatted_posts += "\n\nThis is an automatic post."
    return formatted_posts

if __name__ == "__main__":
    # URL
    github_url = "https://github.com/claromes.atom"

    # Load posted items
    posted_items = load_posted_items()

    # Fetch and post GitHub items
    github_items = fetch_github(github_url)
    new_github_items = [item for item in github_items if not is_item_posted(item['link'], posted_items)]

    if new_github_items:
        github_item_post = format_github_posts(new_github_items)
        linkedin_post(github_item_post)
        posted_items.extend([item['link'] for item in new_github_items])

    # Save updated posted items
    save_posted_items(posted_items)
