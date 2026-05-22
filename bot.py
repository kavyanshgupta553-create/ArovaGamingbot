import json
import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# ==========================================
# SETTINGS
# ==========================================

BOT_TOKEN = os.getenv("8471398768:AAE4uNoCwK1GzGMc_qVpVFCAYX56QOuprTY")

ADMIN_ID = 7428034309
ADMIN_USERNAME = "Kavyanshh2009"

SHOP_NAME = "Arova Gaming"

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# ==========================================
# STATES
# ==========================================

CHOOSING = 1
BUY_BUDGET = 2
ADMIN_ADD = 3

# ==========================================
# DATABASE
# ==========================================

DB_FILE = "ids.json"


def load_ids():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_ids(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==========================================
# MAIN MENU
# ==========================================


def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛒 Buy BGMI ID", callback_data="buy")],
        [InlineKeyboardButton("💰 Sell BGMI ID", callback_data="sell")],
        [InlineKeyboardButton("🆘 Help & Support", callback_data="help")],
    ]

    return InlineKeyboardMarkup(keyboard)


# ==========================================
# START
# ==========================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        f"🎮 Welcome to {SHOP_NAME}\n\n"
        "✅ Trusted IDs\n"
        "⚡ Fast Response\n"
        "🔒 Secure Deals\n\n"
        "Choose option below 👇"
    )

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=main_menu(),
        )

    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=main_menu(),
        )

    return CHOOSING


# ==========================================
# MENU HANDLER
# ==========================================


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # BUY
    if data == "buy":

        await query.edit_message_text(
            "💰 Apna budget bhejo\n\nExample: 2000"
        )

        return BUY_BUDGET

    # SELL
    elif data == "sell":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📩 Contact Admin",
                    url=f"https://t.me/Aayushrajput14"
                )
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await query.edit_message_text(
            "💰 BGMI ID sell karni hai?\n\n"
            "Admin se direct contact karo.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return CHOOSING

    # HELP
    elif data == "help":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🆘 Contact Support",
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await query.edit_message_text(
            "🆘 Help & Support",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return CHOOSING

    elif data == "back":
        return await start(update, context)


# ==========================================
# BUY SYSTEM
# ==========================================


async def buy_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(
            "❌ Sirf number bhejo"
        )
        return BUY_BUDGET

    budget = int(text)

    ids = load_ids()

    matched = []

    for item in ids:
        if item["price"] <= budget + 500:
            matched.append(item)

    if not matched:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📩 Contact Admin",
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ]
        ]

        await update.message.reply_text(
            "😔 Is budget me abhi koi ID available nahi hai.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return CHOOSING

    await update.message.reply_text(
        f"✅ {len(matched)} IDs mili"
    )

    for item in matched:

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔥 Interested",
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ]
        ]

        caption = (
            f"🎮 BGMI ID\n\n"
            f"📊 Level: {item['level']}\n"
            f"🏆 Tier: {item['tier']}\n"
            f"🔫 Skins: {item['skins']}\n"
            f"👕 Outfits: {item['outfits']}\n"
            f"💎 UC: {item['uc']}\n"
            f"💰 Price: ₹{item['price']}"
        )

        if item["photo"]:
            await update.message.reply_photo(
                photo=item["photo"],
                caption=caption,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await update.message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    return CHOOSING


# ==========================================
# ADD ID COMMAND
# ==========================================


async def add_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    text = (
        "New ID add karne ke liye format use karo:\n\n"
        "Level|Tier|Skins|Outfits|UC|Price"
    )

    await update.message.reply_text(text)

    return ADMIN_ADD


# ==========================================
# SAVE ID
# ==========================================


async def save_new_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        text = update.message.text

        parts = text.split("|")

        if len(parts) != 6:
            await update.message.reply_text(
                "❌ Wrong format"
            )
            return ADMIN_ADD

        level, tier, skins, outfits, uc, price = parts

        photo_id = None

        if update.message.reply_to_message:
            if update.message.reply_to_message.photo:
                photo_id = update.message.reply_to_message.photo[-1].file_id

        data = load_ids()

        data.append({
            "level": level,
            "tier": tier,
            "skins": skins,
            "outfits": outfits,
            "uc": uc,
            "price": int(price),
            "photo": photo_id
        })

        save_ids(data)

        await update.message.reply_text(
            "✅ ID Added Successfully"
        )

        return CHOOSING

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        return CHOOSING


# ==========================================
# LIST IDS
# ==========================================


async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    data = load_ids()

    if not data:
        await update.message.reply_text("No IDs")
        return

    msg = "🎮 Current IDs\n\n"

    for i, item in enumerate(data):
        msg += (
            f"{i+1}. ₹{item['price']} | "
            f"{item['tier']} | "
            f"Level {item['level']}\n"
        )

    await update.message.reply_text(msg)


# ==========================================
# UNKNOWN
# ==========================================


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Use /start"
    )


# ==========================================
# MAIN
# ==========================================


def main():

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],

        states={
            CHOOSING: [
                CallbackQueryHandler(menu_handler),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    unknown
                )
            ],

            BUY_BUDGET: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    buy_budget
                )
            ],

            ADMIN_ADD: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_new_id
                )
            ],
        },

        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("addid", add_id))

    application.add_handler(CommandHandler("listids", list_ids))

    print("Bot Running...")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await query.edit_message_text(
            "🆘 Help & Support",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return CHOOSING

    elif data == "back":
        return await start(update, context)


# ==========================================
# BUY SYSTEM
# ==========================================


async def buy_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(
            "❌ Sirf number bhejo"
        )
        return BUY_BUDGET

    budget = int(text)

    ids = load_ids()

    matched = []

    for item in ids:
        if item["price"] <= budget + 500:
            matched.append(item)

    if not matched:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📩 Contact Admin",
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ]
        ]

        await update.message.reply_text(
            "😔 Is budget me abhi koi ID available nahi hai.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return CHOOSING

    await update.message.reply_text(
        f"✅ {len(matched)} IDs mili"
    )

    for item in matched:

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔥 Interested",
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ]
        ]

        caption = (
            f"🎮 BGMI ID\n\n"
            f"📊 Level: {item['level']}\n"
            f"🏆 Tier: {item['tier']}\n"
            f"🔫 Skins: {item['skins']}\n"
            f"👕 Outfits: {item['outfits']}\n"
            f"💎 UC: {item['uc']}\n"
            f"💰 Price: ₹{item['price']}"
        )

        if item["photo"]:
            await update.message.reply_photo(
                photo=item["photo"],
                caption=caption,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        else:
            await update.message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    return CHOOSING


# ==========================================
# ADD ID COMMAND
# ==========================================


async def add_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    text = (
        "New ID add karne ke liye format use karo:\n\n"
        "Level|Tier|Skins|Outfits|UC|Price"
    )

    await update.message.reply_text(text)

    return ADMIN_ADD


# ==========================================
# SAVE ID
# ==========================================


async def save_new_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        text = update.message.text

        parts = text.split("|")

        if len(parts) != 6:
            await update.message.reply_text(
                "❌ Wrong format"
            )
            return ADMIN_ADD

        level, tier, skins, outfits, uc, price = parts

        photo_id = None

        if update.message.reply_to_message:
            if update.message.reply_to_message.photo:
                photo_id = update.message.reply_to_message.photo[-1].file_id

        data = load_ids()

        data.append({
            "level": level,
            "tier": tier,
            "skins": skins,
            "outfits": outfits,
            "uc": uc,
            "price": int(price),
            "photo": photo_id
        })

        save_ids(data)

        await update.message.reply_text(
            "✅ ID Added Successfully"
        )

        return CHOOSING

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        return CHOOSING


# ==========================================
# LIST IDS
# ==========================================


async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    data = load_ids()

    if not data:
        await update.message.reply_text("No IDs")
        return

    msg = "🎮 Current IDs\n\n"

    for i, item in enumerate(data):
        msg += (
            f"{i+1}. ₹{item['price']} | "
            f"{item['tier']} | "
            f"Level {item['level']}\n"
        )

    await update.message.reply_text(msg)


# ==========================================
# UNKNOWN
# ==========================================


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Use /start"
    )


# ==========================================
# MAIN
# ==========================================


def main():

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],

        states={
            CHOOSING: [
                CallbackQueryHandler(menu_handler),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    unknown
                )
            ],

            BUY_BUDGET: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    buy_budget
                )
            ],

            ADMIN_ADD: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_new_id
                )
            ],
        },

        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("addid", add_id))

    application.add_handler(CommandHandler("listids", list_ids))

    print("Bot Running...")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
