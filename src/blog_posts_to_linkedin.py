import feedparser
from bs4 import BeautifulSoup

from utils import load_posted_items, save_posted_items, is_item_posted, linkedin_post

def html_parser(text):
    """Removes HTML tags from a string."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

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

def format_blog_posts(entry):
    """Formats the blog entry for posting."""
    formatted_post = f"{entry['title']}\n\n{entry['description']}\n\nRead more: {entry['link']}\n\nThis is an automatic post."
    return formatted_post

if __name__ == "__main__":
    # URL
    blog_url = "https://claromes.com/feeds/rss.xml"

    # Load posted items
    posted_items = load_posted_items()

    # Fetch and post blog items
    blog_item = fetch_blog(blog_url)
    if blog_item:
        blog_item_id = blog_item['link']
        if not is_item_posted(blog_item_id, posted_items):
            blog_item_post = format_blog_posts(blog_item)
            linkedin_post(blog_item_post)
            posted_items.append(blog_item_id)

    # Save updated posted items
    save_posted_items(posted_items)
