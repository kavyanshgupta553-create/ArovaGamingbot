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

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8471398768:AAHp6XunmwnCrMKPrnKMsxK6Zw2C-Di9ymM")

ADMIN1_ID       = 7428034309      # Buying + Help
ADMIN1_USERNAME = "Kavyanshh2009"

ADMIN2_ID       = 7879442639      # Selling
ADMIN2_USERNAME = "Aayushrajput14"

SHOP_NAME = "Arova Gaming"

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==========================================
# STATES
# ==========================================

CHOOSING   = 1
BUY_BUDGET = 2
ADMIN_ADD  = 3

# ==========================================
# JSON DATABASE
# ==========================================

DB_FILE = "ids.json"

SAMPLE_IDS = [
    {
        "level": "72",
        "tier": "Platinum III",
        "skins": "M416 Glacier, AKM Glacier, DP-28 Coral",
        "outfits": "4 Legendary, 2 Epic Sets",
        "uc": "~12,000 UC",
        "price": 2500,
        "photo": "https://i.imgur.com/3QfIzXL.jpeg"
    },
    {
        "level": "57",
        "tier": "Gold I",
        "skins": "M416 Pharaoh, UMP45 Coral, Kar98 Fool's Gold",
        "outfits": "2 Legendary, 3 Epic Sets",
        "uc": "~5,500 UC",
        "price": 1300,
        "photo": "https://i.imgur.com/FwXmjTH.jpeg"
    },
    {
        "level": "89",
        "tier": "Diamond II",
        "skins": "M416 Glacier, AWM Frost, Groza Egg, Mini14 Coral",
        "outfits": "9 Legendary, 5 Epic Sets",
        "uc": "~22,000 UC",
        "price": 5500,
        "photo": "https://i.imgur.com/vQk3nH1.jpeg"
    },
    {
        "level": "45",
        "tier": "Silver II",
        "skins": "M416 Blood Raven, S12K Flaming",
        "outfits": "1 Legendary",
        "uc": "~2,000 UC",
        "price": 700,
        "photo": "https://i.imgur.com/3QfIzXL.jpeg"
    },
    {
        "level": "95",
        "tier": "Ace",
        "skins": "M416 Glacier, AWM Flaming, Groza Egg, DP-28 Glacier, Vector Glacier",
        "outfits": "15 Legendary, 8 Epic, 1 Mythic Set",
        "uc": "~40,000 UC",
        "price": 9999,
        "photo": "https://i.imgur.com/vQk3nH1.jpeg"
    },
]


def load_ids():
    if not os.path.exists(DB_FILE):
        save_ids(SAMPLE_IDS)
        return SAMPLE_IDS
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return SAMPLE_IDS


def save_ids(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==========================================
# MAIN MENU
# ==========================================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒  Buy BGMI ID",    callback_data="buy")],
        [InlineKeyboardButton("💰  Sell BGMI ID",   callback_data="sell")],
        [InlineKeyboardButton("🆘  Help & Support", callback_data="help")],
    ])


async def show_main_menu(target, context):
    text = (
        f"🎮 *Welcome to {SHOP_NAME}!*\n\n"
        "India's Trusted BGMI ID Marketplace\n\n"
        "✅  100% Safe & Secure\n"
        "⚡  Fast Response\n"
        "🔒  Verified Accounts Only\n\n"
        "What would you like to do? 👇"
    )
    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, reply_markup=main_menu(), parse_mode="Markdown")
    else:
        await target.reply_text(text, reply_markup=main_menu(), parse_mode="Markdown")


# ==========================================
# /start — any message also triggers menu
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    if update.message:
        await show_main_menu(update.message, context)
    else:
        await show_main_menu(update.callback_query, context)
    return CHOOSING


# ==========================================
# MENU HANDLER
# ==========================================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---------- BUY ----------
    if data == "buy":
        await query.edit_message_text(
            "🛒 *Buy a BGMI ID*\n\n"
            "💰 Enter your *budget* in ₹ (numbers only)\n"
            "📌 Example: `2000`\n\n"
            "We'll show IDs at your budget and up to ₹500 above for best deals! 👇",
            parse_mode="Markdown"
        )
        return BUY_BUDGET

    # ---------- SELL ----------
    elif data == "sell":
        kb = [
            [InlineKeyboardButton(
                f"💬  Chat with @{ADMIN2_USERNAME}",
                url=f"https://t.me/{ADMIN2_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Back", callback_data="back")],
        ]
        await query.edit_message_text(
            "💰 *Sell Your BGMI ID*\n\n"
            f"Contact *@{ADMIN2_USERNAME}* directly!\n\n"
            "He will ask for your details and give the best price.\n\n"
            "📋 *Keep these ready:*\n"
            "• BGMI ID & Level\n"
            "• Current Tier\n"
            "• Gun Skins & Outfits\n"
            "• UC Spent (approx)\n"
            "• Screenshot of your account\n\n"
            "⏰ Response time: *10–30 minutes*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        return CHOOSING

    # ---------- HELP ----------
    elif data == "help":
        kb = [
            [InlineKeyboardButton(
                f"🆘  Contact @{ADMIN1_USERNAME}",
                url=f"https://t.me/{ADMIN1_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Back", callback_data="back")],
        ]
        await query.edit_message_text(
            "🆘 *Help & Support*\n\n"
            f"Contact *@{ADMIN1_USERNAME}* for any issue!\n\n"
            "We help with:\n"
            "• Payment problems\n"
            "• Account transfer issues\n"
            "• General queries\n"
            "• After-sale support\n\n"
            "⏰ Response time: *10–30 minutes*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        return CHOOSING

    # ---------- BACK ----------
    elif data == "back":
        await show_main_menu(query, context)
        return CHOOSING

    return CHOOSING


# ==========================================
# BUY — receive budget, show matching IDs
# ==========================================

async def buy_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(
            "❌ *Numbers only please!*\n"
            "📌 Example: `2000`\n\nTry again 👇",
            parse_mode="Markdown"
        )
        return BUY_BUDGET

    budget = int(text)
    upper  = budget + 500
    ids    = load_ids()

    exact   = [i for i in ids if i["price"] <= budget]
    stretch = [i for i in ids if budget < i["price"] <= upper]
    matched = exact + stretch

    # Nothing found
    if not matched:
        kb = [
            [InlineKeyboardButton(
                f"💬  Contact @{ADMIN1_USERNAME}",
                url=f"https://t.me/{ADMIN1_USERNAME}"
            )],
            [InlineKeyboardButton("🔙  Main Menu", callback_data="back")],
        ]
        await update.message.reply_text(
            f"😔 *No IDs available in ₹{budget} budget right now.*\n\n"
            "Contact admin — a custom deal might be possible! 👇",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        return CHOOSING

    # Header
    await update.message.reply_text(
        f"✅ *Found {len(matched)} ID(s) for you!*\n"
        f"💰 Your budget: ₹{budget}  |  🔍 Showing up to ₹{upper}\n\n"
        "Check details below 👇",
        parse_mode="Markdown"
    )

    # Send each ID
    for item in matched:
        is_stretch = item["price"] > budget
        tag = "⚡ *Just Above Budget — Great Value!*\n\n" if is_stretch else ""

        caption = (
            f"{tag}"
            f"🎮 *BGMI Account — {SHOP_NAME}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊  Level: *{item['level']}*\n"
            f"🏆  Tier: *{item['tier']}*\n"
            f"🔫  Skins: {item['skins']}\n"
            f"👕  Outfits: {item['outfits']}\n"
            f"💎  UC Spent: {item['uc']}\n"
            f"💰  Price: *₹{item['price']}*\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )

        kb = [[InlineKeyboardButton(
            "🔥  Interested — Contact Admin",
            url=f"https://t.me/{ADMIN1_USERNAME}"
        )]]

        try:
            if item.get("photo"):
                await update.message.reply_photo(
                    photo=item["photo"],
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    caption,
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.warning(f"Photo failed, sending text instead: {e}")
            await update.message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="Markdown"
            )

    # Footer
    kb = [[InlineKeyboardButton("🔙  Main Menu", callback_data="back")]]
    await update.message.reply_text(
        f"👆 Pick your favourite ID above!\n\n"
        f"🏪 *{SHOP_NAME}* — India's Trusted BGMI Store",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )
    return CHOOSING


# ==========================================
# ADMIN — /addid command
# ==========================================

async def add_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return

    await update.message.reply_text(
        "📝 *Add New ID*\n\n"
        "Send details in this exact format:\n\n"
        "`Level|Tier|Skins|Outfits|UC|Price`\n\n"
        "📌 Example:\n"
        "`72|Platinum III|M416 Glacier, AKM|4 Legendary|12000 UC|2500`\n\n"
        "📸 *To add a photo:*\n"
        "Send the photo first, then reply to it with the above format.",
        parse_mode="Markdown"
    )
    return ADMIN_ADD


async def save_new_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return CHOOSING

    try:
        parts = update.message.text.strip().split("|")
        if len(parts) != 6:
            await update.message.reply_text(
                "❌ *Wrong format!*\n\n"
                "Use exactly: `Level|Tier|Skins|Outfits|UC|Price`",
                parse_mode="Markdown"
            )
            return ADMIN_ADD

        level, tier, skins, outfits, uc, price = [p.strip() for p in parts]

        photo_id = None
        if update.message.reply_to_message and update.message.reply_to_message.photo:
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
            f"✅ *ID Added Successfully!*\n\n"
            f"📊 Level: {level}\n"
            f"🏆 Tier: {tier}\n"
            f"💰 Price: ₹{price}",
            parse_mode="Markdown"
        )
        return CHOOSING

    except ValueError:
        await update.message.reply_text("❌ Price must be a number!")
        return ADMIN_ADD
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        return CHOOSING


# ==========================================
# ADMIN — /listids command
# ==========================================

async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return

    data = load_ids()
    if not data:
        await update.message.reply_text("📭 No IDs in database.")
        return

    msg = f"🎮 *{SHOP_NAME} — ID List*\n\n"
    for i, item in enumerate(data, 1):
        msg += (
            f"{i}. ₹{item['price']} | "
            f"{item['tier']} | "
            f"Level {item['level']}\n"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")


# ==========================================
# ADMIN — /deleteid command
# ==========================================

async def delete_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN1_ID, ADMIN2_ID]:
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "Usage: `/deleteid <number>`\n"
            "Use /listids to see ID numbers.",
            parse_mode="Markdown"
        )
        return

    index = int(context.args[0]) - 1
    data  = load_ids()

    if index < 0 or index >= len(data):
        await update.message.reply_text("❌ Invalid ID number.")
        return

    removed = data.pop(index)
    save_ids(data)

    await update.message.reply_text(
        f"✅ *Deleted:* Level {removed['level']} | "
        f"{removed['tier']} | ₹{removed['price']}",
        parse_mode="Markdown"
    )


# ==========================================
# FALLBACK — any random message → menu
# ==========================================

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update.message, context)
    return CHOOSING


# ==========================================
# MAIN
# ==========================================

def main():
    print(f"🚀 {SHOP_NAME} Bot starting...")

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start),
        ],
        states={
            CHOOSING: [
                CallbackQueryHandler(menu_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, any_message),
            ],
            BUY_BUDGET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, buy_budget),
                CallbackQueryHandler(menu_handler),
            ],
            ADMIN_ADD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_new_id),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            MessageHandler(filters.ALL, start),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("addid",    add_id))
    app.add_handler(CommandHandler("listids",  list_ids))
    app.add_handler(CommandHandler("deleteid", delete_id))

    print(f"✅ {SHOP_NAME} Bot is live!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
