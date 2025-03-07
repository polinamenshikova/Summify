import os
from dotenv import load_dotenv
import openai
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# Load environment variables from the .env file
load_dotenv()

# Set the API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Define conversation state
SUMMARIZING = 1

def generate_summary(text):
    """
    Generates a concise summary with main bullet points for the provided text.
    """
    prompt = (
        f"Please read the following text:\n{text}\n\n"
        "and generate an extremely concise summary in the form of a few short bullet points. "
        "Focus on the absolute key ideas and conclusions, avoiding any extra details. "
        "Keep each bullet point very brief and to the point."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # Change to gpt-4 if you have access
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for the /start command. Initiates the summarization session.
    """
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! You're now in a summarization session. "
        "Send me any text and I'll summarize it for you. Type /cancel to exit the session.",
        reply_markup=ForceReply(selective=True),
    )
    return SUMMARIZING

async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handler for incoming text messages in the summarization session.
    Generates a summary and sends it back to the user.
    """
    user_text = update.message.text
    summary = generate_summary(user_text)
    await update.message.reply_text(summary)
    # Remain in the session so that subsequent texts are summarized without needing /start again
    return SUMMARIZING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ends the summarization session.
    """
    await update.message.reply_text("Summarization session ended. Type /start if you want to begin again.")
    return ConversationHandler.END

def main():
    # Create the Telegram application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Set up the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SUMMARIZING: [MessageHandler(filters.TEXT & ~filters.COMMAND, summarize_text)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
