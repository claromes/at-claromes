import os
import json
import requests

STATE_FILE = "posted_items.json"

def load_posted_items():
    """Loads the list of previously posted items from a JSON file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_posted_items(posted_items):
    """Saves the list of posted items to a JSON file."""
    with open(STATE_FILE, 'w') as file:
        json.dump(posted_items, file)

def is_item_posted(item_id, posted_items):
    """Checks if an item has already been posted."""
    return item_id in posted_items

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
