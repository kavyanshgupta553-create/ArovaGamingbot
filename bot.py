import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
#        AROVA GAMING — BGMI ID BOT
# ==========================================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8471398768:AAE4uNoCwK1GzGMc_qVpVFCAYX56QOuprTY")

ADMIN1_ID       = 7428034309
ADMIN1_USERNAME = "Kavyanshh2009"

ADMIN2_ID       = 7879442639
ADMIN2_USERNAME = "Aayushrajput14"

SHOP_NAME = "Arova Gaming"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# States
CHOOSING   = 1
BUY_BUDGET = 2
ADMIN_ADD  = 3

# ==========================================
# DATABASE
# ==========================================

SAMPLE_IDS = [
    {
        "level": "72",
        "tier": "Platinum III",
        "skins": "M416 Glacier, AKM Glacier, DP-28 Coral",
        "outfits": "4 Legendary, 2 Epic Sets",
        "uc": "~12,000 UC",
        "price": 2500,
        "photo": None,
    },
    {
        "level": "57",
        "tier": "Gold I",
        "skins": "M416 Pharaoh, UMP45 Coral, Kar98 Fool's Gold",
        "outfits": "2 Legendary, 3 Epic Sets",
        "uc": "~5,500 UC",
        "price": 1300,
        "photo": None,
    },
    {
        "level": "89",
        "tier": "Diamond II",
        "skins": "M416 Glacier, AWM Frost, Groza Egg, Mini14 Coral",
        "outfits": "9 Legendary, 5 Epic Sets",
        "uc": "~22,000 UC",
        "price": 5500,
        "photo": None,
    },
    {
        "level": "45",
        "tier": "Silver II",
        "skins": "M416 Blood Raven, S12K Flaming",
        "outfits": "1 Legendary",
        "uc": "~2,000 UC",
        "price": 700,
        "photo": None,
    },
    {
        "level": "95",
        "tier": "Ace",
        "skins": "M416 Glacier, AWM Flaming, Groza Egg, DP-28 Glacier, Vector Glacier",
        "outfits": "15 Legendary, 8 Epic, 1 Mythic Set",
        "uc": "~40,000 UC",
        "price": 9999,
        "photo": None,
    },
]

DB_FILE = "ids.json"
_ids_cache = None


def load_ids():
    global _ids_cache
    if _ids_cache is not None:
        return _ids_cache
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                data = json.load(f)
            if data:
                _ids_cache = data
                return _ids_cache
    except Exception as e:
        logger.warning(f"Could not load ids.json: {e}")
    _ids_cache = list(SAMPLE_IDS)
    return _ids_cache


def save_ids(data):
    global _ids_cache
    _ids_cache = data
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.warning(f"Could not save: {e}")


# ==========================================
# HELPERS
# ==========================================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒  Buy BGMI ID",    callback_data="buy")],
        [InlineKeyboardButton("💰  Sell BGMI ID",   callback_data="sell")],
        [InlineKeyboardButton("🆘  Help & Support", callback_data="help")],
    ])


async def show_menu_message(message):
    await message.reply_text(
        f"🎮 Welcome to {SHOP_NAME}!\n\n"
        "India's Trusted BGMI ID Marketplace\n\n"
        "✅  100% Safe and Secure\n"
        "⚡  Fast Response\n"
        "🔒  Verified Accounts Only\n\n"
        "What would you like to do? 👇",
        reply_markup=main_menu(),
    )


async def show_menu_query(query):
    await query.edit_message_text(
        f"🎮 Welcome to {SHOP_NAME}!\n\n"
        "India's Trusted BGMI ID Marketplace\n\n"
        "✅  100% Safe and Secure\n"
        "⚡  Fast Response\n"
        "🔒  Verified Accounts Only\n\n"
        "What would you like to do? 👇",
        reply_markup=main_menu(),
    )


# ==========================================
# /start
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await show_menu_message(update.message)
    return CHOOSING


# ==========================================
# MENU BUTTONS
# ==========================================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.edit_message_text(
            "🛒 Buy a BGMI ID\n\n"
            "Enter your budget in rupees (numbers only)\n\n"
            "Example: 2000\n\n"
            "We will show IDs at your budget and up to Rs.500 above!"
        )
        return BUY_BUDGET

    elif query.data == "sell":
        kb = [
            [InlineKeyboardButton(
                f"💬  Chat with @{ADMIN2_USERNAME}",
                url=f"https://t.me/{ADMIN2_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Back", callback_data="back")],
        ]
        await query.edit_message_text(
            "💰 Sell Your BGMI ID\n\n"
            f"Contact @{ADMIN2_USERNAME} directly!\n\n"
            "He will ask for your details and give the best price.\n\n"
            "Keep these ready:\n"
            "• BGMI ID and Level\n"
            "• Current Tier\n"
            "• Gun Skins and Outfits\n"
            "• UC Spent (approx)\n"
            "• Screenshot of your account\n\n"
            "Response time: 10 to 30 minutes",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        return CHOOSING

    elif query.data == "help":
        kb = [
            [InlineKeyboardButton(
                f"🆘  Contact @{ADMIN1_USERNAME}",
                url=f"https://t.me/{ADMIN1_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Back", callback_data="back")],
        ]
        await query.edit_message_text(
            "🆘 Help and Support\n\n"
            f"Contact @{ADMIN1_USERNAME} for any issue!\n\n"
            "We help with:\n"
            "• Payment problems\n"
            "• Account transfer issues\n"
            "• General queries\n"
            "• After-sale support\n\n"
            "Response time: 10 to 30 minutes",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        return CHOOSING

    elif query.data == "back":
        await show_menu_query(query)
        return CHOOSING

    return CHOOSING


# ==========================================
# BUY — budget handler
# ==========================================

async def buy_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(
            "Please enter numbers only!\n"
            "Example: 2000\n\n"
            "Try again 👇"
        )
        return BUY_BUDGET

    budget = int(text)
    upper  = budget + 500
    ids    = load_ids()

    matched = [i for i in ids if i["price"] <= upper]

    if not matched:
        kb = [
            [InlineKeyboardButton(
                f"💬  Contact @{ADMIN1_USERNAME}",
                url=f"https://t.me/{ADMIN1_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Main Menu", callback_data="back")],
        ]
        await update.message.reply_text(
            f"No IDs available for Rs.{budget} right now.\n\n"
            "Contact admin for a custom deal!",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        return CHOOSING

    await update.message.reply_text(
        f"Found {len(matched)} ID(s) for you!\n"
        f"Budget: Rs.{budget} | Showing up to Rs.{upper}\n\n"
        "Check details below 👇"
    )

    for item in matched:
        is_stretch = item["price"] > budget
        tag = "Just Above Budget — Great Value!\n\n" if is_stretch else ""

        text_card = (
            f"{tag}"
            f"BGMI Account — {SHOP_NAME}\n"
            f"====================\n"
            f"Level    : {item['level']}\n"
            f"Tier     : {item['tier']}\n"
            f"Skins    : {item['skins']}\n"
            f"Outfits  : {item['outfits']}\n"
            f"UC Spent : {item['uc']}\n"
            f"Price    : Rs.{item['price']}\n"
            f"===================="
        )

        kb = [[InlineKeyboardButton(
            "🔥  Interested — Contact Admin",
            url=f"https://t.me/{ADMIN1_USERNAME}"
        )]]

        photo = item.get("photo")
        if photo:
            try:
                await update.message.reply_photo(
                    photo=photo,
                    caption=text_card,
                    reply_markup=InlineKeyboardMarkup(kb),
                )
                continue
            except Exception as e:
                logger.warning(f"Photo failed: {e}")

        await update.message.reply_text(
            text_card,
            reply_markup=InlineKeyboardMarkup(kb),
        )

    await update.message.reply_text(
        f"Pick your favourite ID and contact admin!\n"
        f"{SHOP_NAME} — India's Trusted BGMI Store",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙  Main Menu", callback_data="back")]]
        ),
    )
    return CHOOSING


# ==========================================
# ADMIN COMMANDS
# ==========================================

async def add_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        await update.message.reply_text("You are not authorized.")
        return ConversationHandler.END

    await update.message.reply_text(
        "Send ID details in this format:\n\n"
        "Level|Tier|Skins|Outfits|UC|Price\n\n"
        "Example:\n"
        "72|Platinum III|M416 Glacier, AKM|4 Legendary|12000 UC|2500\n\n"
        "To add photo: send photo first, then reply to it with format above."
    )
    return ADMIN_ADD


async def save_new_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return CHOOSING

    try:
        parts = update.message.text.strip().split("|")
        if len(parts) != 6:
            await update.message.reply_text(
                "Wrong format! Use exactly:\n"
                "Level|Tier|Skins|Outfits|UC|Price"
            )
            return ADMIN_ADD

        level, tier, skins, outfits, uc, price = [p.strip() for p in parts]

        photo_id = None
        if (
            update.message.reply_to_message
            and update.message.reply_to_message.photo
        ):
            photo_id = update.message.reply_to_message.photo[-1].file_id

        data = load_ids()
        data.append({
            "level":   level,
            "tier":    tier,
            "skins":   skins,
            "outfits": outfits,
            "uc":      uc,
            "price":   int(price),
            "photo":   photo_id,
        })
        save_ids(data)

        await update.message.reply_text(
            f"ID Added Successfully!\n"
            f"Level: {level} | Tier: {tier} | Rs.{price}"
        )
        return CHOOSING

    except ValueError:
        await update.message.reply_text("Price must be a number! Try again.")
        return ADMIN_ADD
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        return CHOOSING


async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return
    data = load_ids()
    if not data:
        await update.message.reply_text("No IDs in database.")
        return
    msg = f"{SHOP_NAME} — All IDs\n\n"
    for i, item in enumerate(data, 1):
        msg += f"{i}. Rs.{item['price']} | {item['tier']} | Level {item['level']}\n"
    await update.message.reply_text(msg)


async def delete_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "Usage: /deleteid <number>\nUse /listids to see numbers."
        )
        return
    index = int(context.args[0]) - 1
    data  = load_ids()
    if index < 0 or index >= len(data):
        await update.message.reply_text("Invalid number.")
        return
    removed = data.pop(index)
    save_ids(data)
    await update.message.reply_text(
        f"Deleted: Level {removed['level']} | {removed['tier']} | Rs.{removed['price']}"
    )


# ==========================================
# UNKNOWN MESSAGE in CHOOSING state
# ==========================================

async def unknown_in_choosing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu_message(update.message)
    return CHOOSING


# ==========================================
# MAIN
# ==========================================

def main():
    print(f"Starting {SHOP_NAME} Bot...")

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            CHOOSING: [
                CallbackQueryHandler(menu_handler),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    unknown_in_choosing
                ),
            ],
            BUY_BUDGET: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    buy_budget
                ),
                CallbackQueryHandler(menu_handler),
            ],
            ADMIN_ADD: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_new_id
                ),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
        ],
        allow_reentry=False,
        per_message=False,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("addid",    add_id))
    app.add_handler(CommandHandler("listids",  list_ids))
    app.add_handler(CommandHandler("deleteid", delete_id))

    print(f"{SHOP_NAME} Bot is live!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
