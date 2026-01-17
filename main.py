from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise RuntimeError('BOT_TOKEN env-var is not set')

import telebot
from telebot.types import Message
from guess_fig import get_prediction

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    cid = message.chat.id
    # optional: remember this chat
    bot.send_message(
        cid,
        "👋 Hi! I'm alive and listening. "
        "Use /help to see what I can do."
    )

@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = (
        "*Geo-Shape Bot Help*\n"
        "Send me any picture that contains a *single, clearly-drawn* geometric shape and I'll try to tell you which one it is.\n\n"
        "Supported shapes:\n"
        "• circle\n"
        "• oval\n"
        "• semicircle\n"
        "• triangle\n"
        "• square\n"
        "• rectangle\n"
        "• rhombus\n"
        "• parallelogram\n"
        "• trapezoid\n"
        "• kite\n"
        "• pentagon, hexagon, heptagon, octagon, nonagon, decagon\n"
        "• star\n\n"
        "Tips for best results:\n"
        "– Use clean lines on a plain background\n"
        "– Make sure the shape is closed and fully visible\n"
        "– Send only one shape per image\n\n"
        "Commands:\n"
        "/start – wake me up\n"
        "/help  – show this message"
    )
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open('my_figure.png', 'wb') as f:
        f.write(downloaded)

    bot.reply_to(message, get_prediction())


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
