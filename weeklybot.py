from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime
import pytz

TOKEN = '7083104022:AAG7Q2dWOPyq5N1Do3IhaMeq7zGWiHycaRo'
MESSAGE = "ACCOUNTABILITY CHECK\n\nWho did you reach out to last week? Any response?\n\nWho will you be reaching out to this week?"

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! I am your bot, ready to send reminders.')
    context.chat_data['chat_id'] = update.message.chat_id

def send_now(update: Update, context: CallbackContext):
    """Send the message immediately when /go is used."""
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=MESSAGE)

def send_weekly_message(context: CallbackContext):
    """Function to send the weekly message."""
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text=MESSAGE)

def schedule_message(job_queue, chat_id):
    """Schedule the weekly message using JobQueue."""
    phtime = pytz.timezone('Asia/Manila')
    # Target time: Monday at 9 AM PHT
    time = datetime.time(hour=23, minute=7, second=0, tzinfo=phtime)
    job_queue.run_daily(send_weekly_message, time, days=(6,), context=chat_id)

def main():
    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("go", send_now))

    # Example chat ID, replace with actual chat ID or fetch dynamically
    chat_id = '-1002076218797'
    schedule_message(updater.job_queue, chat_id)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
