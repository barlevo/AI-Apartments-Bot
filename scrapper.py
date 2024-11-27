import requests

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Replace with your Facebook Graph API access token
GROUP_ID = "YOUR_GROUP_ID"  # Replace with the Facebook Group ID
GRAPH_API_BASE = "https://graph.facebook.com/v17.0"

def get_group_posts(group_id, access_token, limit=10):
    """
    Scrape posts from a Facebook group using the Graph API.

    Args:
        group_id (str): The ID of the Facebook group.
        access_token (str): Access token for the Facebook Graph API.
        limit (int): The number of posts to fetch.

    Returns:
        list[dict]: A list of dictionaries containing post details.
    """
    url = f"{GRAPH_API_BASE}/{group_id}/feed"
    params = {
        "access_token": access_token,
        "fields": "id,message,created_time,from{id,name},attachments{media}",
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching posts: {response.status_code} - {response.text}")
        return []
    
    data = response.json().get("data", [])
    posts = []
    
    for post in data:
        post_details = {
            "poster_id": post.get("from", {}).get("id"),
            "post_id": post.get("id"),
            "time_published": post.get("created_time"),
            "content": post.get("message", ""),
            "image_url": None  # Default if no image
        }
        
        # Check for media attachments
        attachments = post.get("attachments", {}).get("data", [])
        for attachment in attachments:
            media = attachment.get("media", {})
            if "image" in media:
                post_details["image_url"] = media.get("image", {}).get("src")
                break
        
        posts.append(post_details)
    
    return posts

# Example Usage
# if __name__ == "__main__":
#     posts = get_group_posts(GROUP_ID, ACCESS_TOKEN, limit=5)

