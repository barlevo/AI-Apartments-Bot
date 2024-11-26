import spacy
import regex
import re


def parsed_scraped_data(json_data):
    """
    Parse JSON data to extract metadata and content.

    Args:
        json_data (dict): JSON-like data from the scraper.

    Returns:
        dict: Parsed metadata and content.
    """
    parsed_data = {
        "post_id": json_data.get("post_id"),
        "poster_id": json_data.get("poster_id"),
        "timestamp": json_data.get("timestamp"),
        "images": json_data.get("images", []),
        "content": json_data.get("content", "")
    }
    return parsed_data

# if __name__ == "__main__":
#     scraper_data = {
#         "post_id": "12345",
#         "poster_id": "67890",
#         "content": "מתפנה דירת 3 חדרי שינה ברב הרצוג 4...",
#         "timestamp": "2024-11-23T10:00:00Z",
#         "images": ["image_url1", "image_url2"]
#     }
#     print(parse_json(scraper_data))

