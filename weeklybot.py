import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import schedule
import time
import threading


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7083104022:AAG7Q2dWOPyq5N1Do3IhaMeq7zGWiHycaRo'

CHAT_ID = '-1002076218797'
MESSAGE = "ACCOUNTABILITY CHECK\n\nWho did you reach out to last week? Any response?\n\nWho will you be reaching out to this week?"

def send_message(context: CallbackContext):
    """Function to send the message."""
    context.bot.send_message(chat_id=CHAT_ID, text=MESSAGE)
    logger.info(f"Message sent to {CHAT_ID}")

def schedule_weekly_message(updater):
    """Schedule the weekly message."""
    # Schedule to send the message every Monday at 09:00 AM
    job = schedule.every().monday.at("09:00").do(send_message, context=updater.job_queue)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start(update: Update, context: CallbackContext):
    """Start command."""
    update.message.reply_text('Hi! I will send you a weekly reminder every Monday at 9:00 AM.')
    # Start the background thread for scheduling
    thread = threading.Thread(target=schedule_weekly_message, args=(context.bot,))
    thread.start()

def main():
    """Main function to start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()