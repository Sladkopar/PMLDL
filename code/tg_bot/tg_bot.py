# Test the bot

TOKEN = "your_token"

import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


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

    application.add_handler(MessageHandler(filters.ALL, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
