
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/your_channel")],
        [InlineKeyboardButton("🎬 Movie Channel", url="https://t.me/your_movie_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "မင်္ဂလာပါခင်ဗျာ! FlickZone Movie Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ဤဘော့တ်မှတစ်ဆင့် ရုပ်ရှင်နှင့် ဇာတ်ကားများကို ရှာဖွေကြည့်ရှုနိုင်ပါသည်။"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# /publish command handler for admins
async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Admin ID ကို စစ်ဆေးလိုပါက ထည့်နိုင်သည်၊ လက်ရှိတွင် ပုံစံထုတ်ပေးထားပါသည်။
    args = context.args
    if not args:
        await update.message.reply_text(
            "ကျေးဇူးပြု၍ ပုံစံမှန်ကန်စွာ ပို့ပေးပါ။\n"
            "ဥပမာ - /publish Title | Genre | Synopsis"
        )
        return

    text_data = " ".join(args)
    parts = text_data.split("|")
    
    title = parts[0].strip() if len(parts) > 0 else "Movie Title"
    genre = parts[1].strip() if len(parts) > 1 else "Action, Drama"
    synopsis = parts[2].strip() if len(parts) > 2 else "ဇာတ်လမ်းအကျဉ်း..."

    disclaimer = "\n\n⚠️ သတိပြုရန် - ဤဇာတ်ကားဖိုင်သည် ၅ မိနစ်အတွင်း အလိုအလျောက် ပျက်သွားမည် ဖြစ်ပါသည်။ ပျောက်ဆုံးသွားခြင်း မရှိစေရန်အတွက် မိမိ၏ 'Saved Messages' တွင် သိမ်းထားပေးပါခင်ဗျာ။"
    
    caption = (
        f"🎬 **{title}**\n\n"
        f"🏷 **Genre:** {genre}\n\n"
        f"📖 **Synopsis:** {synopsis}"
        f"{disclaimer}"
    )

    keyboard = [
        [InlineKeyboardButton("🔄 GET FILE AGAIN!", callback_data="get_file")],
        [InlineKeyboardButton("📢 Channel Link", url="https://t.me/your_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # အကယ်၍ Video နှင့်အတူ ပို့လိုပါက Video Caption ဖြင့် ပို့နိုင်ပါသည်။
    await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("publish", publish))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
