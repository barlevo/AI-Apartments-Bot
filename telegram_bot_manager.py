import time
from google.cloud import firestore
from telegram import Bot
import db_manager
import asyncio


TELEGRAM_BOT_TOKEN = "7570728561:AAElM8WqUijERLANn_eo5wyscZLAC8mNjJY"  # Replace with your bot token
CHAT_ID = 380578641  # Replace with the user chat ID (or handle dynamic subscriptions)

bot = Bot(token=TELEGRAM_BOT_TOKEN)



async def send_apartment_details(chat_id, apartment):
    """
    Send apartment details and image to a Telegram user.
    Args:
        chat_id (int): Telegram chat ID of the user.
        apartment (dict): Apartment details to send.
    """
    content = apartment.get("content", "No details available.")
    image_url = apartment.get("image_url", None)

    if image_url:
        await bot.send_photo(chat_id=chat_id, photo=image_url, caption=content)
    else:
        await bot.send_message(chat_id=chat_id, text="content")

async def send_message():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    new_posts = db_manager.fetch_all_apartments()

        # Send posts to the user
    for post in new_posts:
        await bot.send_message(chat_id=CHAT_ID, text=post.get("content", "No details available."))
        # send_apartment_details(CHAT_ID, post)


# if __name__ == "__main__":
#     asyncio.run(send_message())
