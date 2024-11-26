from google.cloud import firestore
from google.oauth2 import service_account
import json 
# Initialize Firestore client
# db = firestore.Client()

key_path = "C:\\Users\\97250\\Desktop\\Scrapper\\ApartmentsBot\\AI-Apartments-Bot\\apartments-bot-442611-45bb23a39491.json"

# Initialize Firestore client with explicit credentials
credentials = service_account.Credentials.from_service_account_file(key_path)
db = firestore.Client(credentials=credentials)


def store_summary(parsed_data, summary):
    """
    Store parsed metadata and LLM summary in the Firestore database.

    Args:
        parsed_data (dict): Parsed metadata from the post.
        summary (dict): LLM-generated summary of the post.

    Returns:
        str: Document ID of the stored data.
    """
    # Merge parsed data and summary into a single object
    # data_to_store = {
    #     **parsed_data,
    #     "summary": summary
    # }
    # Add data to the 'apartments' collection
    # doc_ref = db.collection("apartments").add(data_to_store)
    parsed_data["summary"] = json.dumps(summary)

    doc_ref = db.collection("apartments").add(parsed_data)
    return doc_ref[1].id

def fetch_apartment(post_id):
    """
    Fetch an apartment document by its post ID.

    Args:
        post_id (str): The post ID of the document to retrieve.

    Returns:
        dict: Retrieved document data or None if not found.
    """
    docs = db.collection("apartments").where("post_id", "==", post_id).stream()
    for doc in docs:
        apartment = doc.to_dict()
        # Deserialize summary if it's stored as a string
        if "summary" in apartment and isinstance(apartment["summary"], str):
            try:
                apartment["summary"] = json.loads(apartment["summary"])
            except json.JSONDecodeError as e:
                print(f"Error deserializing summary: {e}")
        return apartment
    return None

def fetch_all_apartments():
    """
    Fetch all apartment documents from the Firestore database.

    Returns:
        list: List of all documents as dictionaries.
    """
    apartments = []
    docs = db.collection("apartments").stream()
    for doc in docs:
        apartments.append(doc.to_dict())
    return apartments

def delete_apartment(post_id):
    """
    Delete an apartment document by its post ID.

    Args:
        post_id (str): The post ID of the document to delete.

    Returns:
        bool: True if a document was deleted, False otherwise.
    """
    docs = db.collection("apartments").where("post_id", "==", post_id).stream()
    for doc in docs:
        db.collection("apartments").document(doc.id).delete()
        return True
    return False

def update_apartment(post_id, updates):
    """
    Update specific fields in an apartment document by its post ID.

    Args:
        post_id (str): The post ID of the document to update.
        updates (dict): Dictionary of fields to update.

    Returns:
        bool: True if a document was updated, False otherwise.
    """
    docs = db.collection("apartments").where("post_id", "==", post_id).stream()
    for doc in docs:
        db.collection("apartments").document(doc.id).update(updates)
        return True
    return False


def test_firestore():
    # Initialize Firestore client
    # db = firestore.Client()

    # Data to test storing
    test_data = {
        "post_id": "test123",
        "poster_id": "poster123",
        "timestamp": "2024-11-23T10:00:00Z",
        "content": "This is a test post for Firestore storage.",
        "summary": {
            "rooms": 2,
            "living_room": "yes",
            "specs": ["balcony", "garden"],
            "price": 1200,
            "contact_info": "Contact: 123-456-7890"
        }
    }

    # Add test data to the 'apartments' collection
    doc_ref = db.collection("apartments").add(test_data)
    doc_id = doc_ref[1].id
    print(f"Test data stored with document ID: {doc_id}")

    # Retrieve the stored data
    retrieved_doc = db.collection("apartments").document(doc_id).get()
    if retrieved_doc.exists:
        print("Retrieved Data:")
        print(retrieved_doc.to_dict())
    else:
        print("Document not found!")

# # Run the test
# if __name__ == "__main__":
#     test_firestore()
