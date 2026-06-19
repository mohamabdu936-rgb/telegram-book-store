from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ضع توكن البوت هنا
TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"

# ضع ID حسابك هنا
OWNER_ID = 123456789

BOOK_TITLE = "Laugh with Your Brain"
SERIES_NAME = "Laugh with Illness Series"
VOLUME = "Volume 1"

SUPPORT_LINK = "https://t.me/Rasha2762"

PRICE = "5 USDT"

WALLET_ADDRESS = "TS3z9oKUcQd9iMSmbjg8h8qHFotu4tEEWe"

SAMPLE_FILE = "sample.pdf"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📖 Free Sample", callback_data="sample")],
        [InlineKeyboardButton("💰 Buy Book", callback_data="buy")],
        [InlineKeyboardButton("💬 Support", callback_data="support")],
    ]

    text = (
        f"Welcome to {SERIES_NAME}\n\n"
        f"{VOLUME}\n"
        f"{BOOK_TITLE}"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "sample":

        with open(SAMPLE_FILE, "rb") as pdf:
            await query.message.reply_document(
                document=pdf,
                caption=f"Free Sample - {BOOK_TITLE}"
            )

    elif query.data == "buy":

        await query.message.reply_text(
            f"📚 {SERIES_NAME}\n"
            f"{VOLUME}\n"
            f"{BOOK_TITLE}\n\n"
            f"💰 Price: {PRICE}\n\n"
            f"Wallet Address:\n"
            f"{WALLET_ADDRESS}\n\n"
            f"After payment, send a screenshot of the transaction here."
        )

    elif query.data == "support":

        await query.message.reply_text(
            f"Support:\n{SUPPORT_LINK}"
        )


async def receive_payment_proof(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.message.from_user

    caption = (
        f"New payment proof\n\n"
        f"User ID: {user.id}\n"
        f"Username: @{user.username}"
    )

    await context.bot.send_photo(
        chat_id=OWNER_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption
    )

    await update.message.reply_text(
        "Your payment proof has been received and is under review."
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receive_payment_proof
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
