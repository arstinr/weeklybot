from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
import datetime

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! I am your bot, ready to send reminders.')
    context.chat_data['chat_id'] = update.message.chat_id

def send_weekly_message(context: CallbackContext):
    """Function to send the weekly message."""
    job = context.job
    context.bot.send_message(chat_id=job.context, text="Hello, this is your weekly reminder!")

def send_now(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Sending this now to make sure it works")

def schedule_message(job_queue):
    """Schedule the weekly message using JobQueue."""
    # Target time: Monday at 9 AM
    time = datetime.time(hour=9, minute=0, second=0)
    # context argument is used to pass the chat_id
    job_queue.run_daily(send_weekly_message, time, days=(0,), context='-1002076218797')  # Example chat_id

def main():
    """Main function to start the bot."""
    TOKEN = '7083104022:AAG7Q2dWOPyq5N1Do3IhaMeq7zGWiHycaRo'
    updater = Updater(TOKEN, use_context=True)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("go", send_now))


    # Schedule messages
    chat_id = '-1002076218797'
    schedule_message(updater.job_queue)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
