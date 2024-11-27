from parser import parsed_scraped_data
from llm_proccesser import summarize_apartment_post
import db_manager
from db_manager import store_summary
import telegram_bot_manager
import asyncio
import time
from telegram import Bot
from googlemaps import Client as GoogleMaps
import json 
import scrapper


TELEGRAM_BOT_TOKEN = "7570728561:AAElM8WqUijERLANn_eo5wyscZLAC8mNjJY"  # Replace with your bot token
CHAT_ID = 380578641  # Replace with the user chat ID (or handle dynamic subscriptions)
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def generate_google_maps_link(address):
    """
    Generate a Google Maps search link for the given address.

    Args:
        address (str): The address to search for on Google Maps.

    Returns:
        str: A Google Maps search link.
    """
    base_url = "https://www.google.com/maps/search/?api=1&query="
    # Replace spaces in the address with "+" for the query parameter
    formatted_address = address.replace(" ", "+")
    return f"{base_url}{formatted_address}"

def generate_contact_link(poster_id, phone_number):
    if phone_number:
        whatsapp_link = f"https://wa.me/{phone_number}"
        return whatsapp_link
    else:
        fb_link = f"https://facebook.com/{poster_id}"
        return fb_link

def format_apartment_message(post, summary):
    """
    Format the bot message with the desired output structure.
    """
    contact_link = generate_contact_link(post["content"], post["poster_id"])
    post_id = post["post_id"]
    post_link =  f"https://facebook.com/{post_id}"
    def bold_labels(summary1):
        lines = summary1.strip().split("\n")
        formatted_lines = []
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                formatted_lines.append(f"**{key.strip()}**: {value.strip()}")
            else:
                formatted_lines.append(line)
        return "\n".join(formatted_lines)

    formatted_summary = bold_labels(summary)



    message = f"""
    🏠 **Apartment Details** 🏠
    
    **Summary**:\n

    ** Published at **: {post.get("timestamp", "N/A")}

    {summary}
    **Original Post: [Click here]({post_link})
    **Contact the Poster**: [Click here]({contact_link})
    """
    return message

def query_database(max_price, min_rooms):
    """
    Query the database for apartments matching the user's criteria.
    This function should interact with your Firestore database.
    """
    from google.cloud import firestore

    db = firestore.Client()
    apartments = []
    docs = db.collection("apartments").where("price", "<=", max_price).where("rooms", ">=", min_rooms).stream()
    for doc in docs:
        apartments.append(doc.to_dict())
    return apartments


async def send_message():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    new_posts = db_manager.fetch_all_apartments()

        # Send posts to the user
    for post in new_posts:
        await bot.send_message(chat_id=CHAT_ID, text=post.get("summary", "No details available."))


async def main(scraper_data):
    # Parse JSON data from scraper
    parsed_data = parsed_scraped_data(scraper_data)

    # Summarize content using LLM
    summary = summarize_apartment_post(parsed_data["content"])
    # parsed_data["summary"] = summary
    # Store in database
    store_summary(parsed_data, summary)
    # Format and print the message
    formatted_message = format_apartment_message(parsed_data, summary)
    await bot.send_message(chat_id=CHAT_ID, text=formatted_message)
    images = parsed_data["images"]
    if images:
        for image_url in images:
            await bot.send_photo(chat_id=CHAT_ID, photo=image_url)


# Example usage
if __name__ == "__main__":
    scraper_data = {
        "post_id": "123456",
        "poster_id": "67890",
        "content": """
    מתפנה דירת 3 חדרי שינה ברב הרצוג 4 (על הרב ברלין/ עזה).
    צמוד לרחוב עזה, עמק המצלבה ותחנות אוטובוס למרכז העיר ולקמפוסים השונים בעיר.
    בדירה 3 חדרי שינה גדולים, מרפסת חיצונית, מרפסת סגורה, סלון קטן ודוד שמש.
    מציעים למכירה מכונת כביסה וטלוויזיה שנקנו כשנכנסו לדירה וחלק מהציוד בחדרים.
    שכ"ד 1900 לשותף, ועד 50 (לכל הדירה). כניסה ב01/09.
    מראים בשלישי בערב בתיאום מראש. מוזמנים לפנות בפרטי.
    """,
        "timestamp": "2024-11-23T10:00:00Z",
        "images": ["https://scontent.ftlv5-1.fna.fbcdn.net/v/t39.30808-6/362982969_10210236789674207_1095376783910432738_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=0_Hr6obVZocQ7kNvgH8WZAc&_nc_zt=23&_nc_ht=scontent.ftlv5-1.fna&_nc_gid=AgJV1-of8DUnJBy8-Ls91iS&oh=00_AYCHh-hTn6qZZFfc0TisWaX6RAkk7saHMU1916luzkSj_g&oe=674BEF3C", "https://scontent.ftlv5-1.fna.fbcdn.net/v/t39.30808-6/362909735_10210236790714233_8882311300982684114_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=mDl8G8i4HqYQ7kNvgEjM7Dp&_nc_zt=23&_nc_ht=scontent.ftlv5-1.fna&_nc_gid=AA_oPT4m-gacRrFz1b8-2qs&oh=00_AYAQf-HklqmSOlo9VlRX685yV8g1o0cp5BDaJ5q2JU0dCQ&oe=674C10DF"]
    }
    scraper_data2 = {        "post_id": "123456",
        "poster_id": "727527332",
        "content": """
                להשכרה: 
                *חוזה לשנה בלבד* 
                ללא הבטחה להארכה מעבר לזה. 
                כניסה מיידית.
                מתאים גם לשותפים או למשפחה קטנה (ילד/ה 1)
                פרטים נוספים בשיחה.
                דירת שלושה חדרים בשכונת רחביה בירושלים, קרובה להכל. 3 כיווני אוויר, מרפסת ומרפסת שירות, חצר פרטית, קומה ראשונה (5 מדרגות מעל מפלס הרחוב).
                6200 ש"ח. תיתכן גמישות מסויימת במחיר למתאימים.
                לפרטים נוספים וסיור וירטואלי - אפשר לפנות בהודעת ווטסאפ 0544242083.    """,
        "timestamp": "2024-11-25T10:00:00Z",
        "images": ["https://scontent.ftlv5-1.fna.fbcdn.net/v/t39.30808-6/465655533_10160608263907333_5833313546981564992_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=IAQCGt58Q7kQ7kNvgH1Zi5I&_nc_zt=23&_nc_ht=scontent.ftlv5-1.fna&_nc_gid=AosGkevt4TvL_bcj5hHNpcJ&oh=00_AYChyzZKhC2U4xMghj25asIYLL3qCDaC7aKoLTekM7H2TA&oe=674CBEBC","https://scontent.ftlv5-1.fna.fbcdn.net/v/t39.30808-6/465740931_10160608263627333_3874022051391065882_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=OPf2SoKXc-QQ7kNvgFfbUoY&_nc_zt=23&_nc_ht=scontent.ftlv5-1.fna&_nc_gid=A62NPSre2wroTnJgp0vhfj_&oh=00_AYBEifI5nYLsEDhEoUa1UE04MYju9ysX1-0az3kOa_OtWA&oe=674CD7B7","https://scontent.ftlv5-1.fna.fbcdn.net/v/t39.30808-6/465788664_10160608264347333_8057974713636089944_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=_RSPMIngjKEQ7kNvgEp7llA&_nc_zt=23&_nc_ht=scontent.ftlv5-1.fna&_nc_gid=A8VJ_7JV5AeRvU6CIvARI7A&oh=00_AYDRd40qzZJaw1g8dUaf1D0cU0WPwC4fQcYGIGAvIZ0cYQ&oe=674CC162"]
}
    # scrapper.get_group_posts()
    asyncio.run(main(scraper_data2))

