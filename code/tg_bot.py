import logging
from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from recsys import RecSys


# Read token and recommendation system credentials
TOKEN = open('tg_bot/token.txt').read().strip()
CLIENT_ID = open('tg_bot/clientID.txt').read().strip()
CLIENT_SECRET = open('tg_bot/clientSecret.txt').read().strip()

# Initialize recommendation system
# rec_sys = RecSys(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a state to track user input
GET_RECOMMENDATIONS_STATE = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Use /help to see options."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_main_buttons(update, edit=False)

async def show_main_buttons(update: Update, edit: bool = True) -> None:
    """Show main options with inline buttons."""
    keyboard = [
        [
            InlineKeyboardButton("Add preferences", callback_data='add_preferences'),
            InlineKeyboardButton("My preferences", callback_data='my_preferences'),
            InlineKeyboardButton("Get recommendations", callback_data='get_recommendations'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if editing an existing message or sending a new one
    if edit:
        await update.callback_query.edit_message_text("Please choose an option:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()

    # Define the 'Back' button
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data='back')]
    ])

    if query.data == 'get_recommendations':
        # Ask the user for the song name
        user_id = query.from_user.id
        GET_RECOMMENDATIONS_STATE[user_id] = True
        await query.edit_message_text("Please send me the name of a song to get recommendations.")
    elif query.data == 'back':
        await show_main_buttons(update, edit=True)
    else:
        await query.edit_message_text("This functionality is under development.", reply_markup=back_button)



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message_text = update.message.text

    if user_id in GET_RECOMMENDATIONS_STATE and GET_RECOMMENDATIONS_STATE[user_id]:
        # Reset the state
        GET_RECOMMENDATIONS_STATE.pop(user_id)

        # Fetch recommendations
        try:
            recommendations = rec_sys.recommend(track_name=message_text, top_k=5)
            if recommendations.empty:
                await update.message.reply_text("No recommendations found for the provided song.")
            else:
                # Format recommendations
                recommendation_text = "\n\n".join(
                    f"🎵 *{row['name']}*\n   💿 Album: {row['album']}\n   🎤 Artists: {', '.join(row['artists'])}\n   🔢 Track Number: {row['track_number']}"
                    for _, row in recommendations.iterrows()
                )
                await update.message.reply_text(f"Here are your recommendations:\n\n{recommendation_text}", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error fetching recommendations: {e}")
            await update.message.reply_text("An error occurred while fetching recommendations. Please try again.")

    else:
        await update.message.reply_text("I didn't understand that. Use /help to see available options.")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
