import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7656444252:AAEF5KzGXvj-BO8mqmbfqu8D-uujWVbB2ks"

# Remove.bg API Key
REMOVEBG_API_KEY = "gKPFCY43fmqVFHqtAuHgM17g"

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the bot is started."""
    update.message.reply_text(
        "Welcome to the Background Remover Bot! Send me an image, and I'll remove its background for you."
    )

def remove_background(image_path: str) -> str:
    """Remove the background of an image using the Remove.bg API."""
    url = "https://api.remove.bg/v1.0/removebg"
    with open(image_path, "rb") as image_file:
        response = requests.post(
            url,
            files={"image_file": image_file},
            data={"size": "auto"},
            headers={"X-Api-Key": REMOVEBG_API_KEY},
        )
    if response.status_code == 200:
        output_file = "output.png"
        with open(output_file, "wb") as file:
            file.write(response.content)
        return output_file
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def handle_image(update: Update, context: CallbackContext) -> None:
    """Handle incoming images."""
    photo_file = update.message.photo[-1].get_file()
    input_file = "input.jpg"
    photo_file.download(input_file)

    try:
        output_file = remove_background(input_file)
        with open(output_file, "rb") as file:
            update.message.reply_photo(photo=file, caption="Here's your image with the background removed!")
    except Exception as e:
        update.message.reply_text(f"Failed to process the image. Error: {e}")

def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
