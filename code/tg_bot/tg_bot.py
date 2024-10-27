import logging
from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Read token from token.txt
TOKEN = open('token.txt').read().strip()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Test file
test_audio = 'test_music.mp3'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Please, check out this song!",
        reply_markup=ForceReply(selective=True),
    )

    await update.message.reply_audio(audio=test_audio)

    await update.message.reply_text("Type /help to see the list of commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")
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
    """Handle button clicks and show the 'Back' button."""
    query = update.callback_query
    await query.answer()

    # Define the 'Back' button
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data='back')]
    ])

    # Show a response (will be thought over and changed)
    if query.data == 'add_preferences':
        await query.edit_message_text("Functionality for 'Add preferences' will be added soon.", reply_markup=back_button)
    elif query.data == 'my_preferences':
        await query.edit_message_text("Functionality for 'My preferences' will be added soon.", reply_markup=back_button)
    elif query.data == 'get_recommendations':
        await query.edit_message_text("Functionality for 'Get recommendations' will be added soon.", reply_markup=back_button)
    elif query.data == 'back':
        # Show main buttons again when "Back" is clicked
        await show_main_buttons(update, edit=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message

    # Log the message details: time, user, and message content
    logger.info(
        f"Message received at {message.date} from {user.username} ({user.id}): {message.text if message.text else '[Non-text message]'}")

    # Check message types and respond accordingly
    if message.text:
        await message.reply_text(message.text)
    elif message.photo:
        await message.reply_photo(photo=message.photo[-1].file_id)  # Send back the largest photo
    elif message.sticker:
        await message.reply_sticker(sticker=message.sticker.file_id)
    elif message.document:
        await message.reply_document(document=message.document.file_id)
    elif message.video:
        await message.reply_video(video=message.video.file_id)
    elif message.audio:
        await message.reply_audio(audio=message.audio.file_id)
    else:
        await message.reply_text("Unsupported message type.")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
