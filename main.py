import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ⚠️ အောက်ပါနေရာနှစ်ခုတွင် မိမိ၏ တကယ့် Telegram Channel Link အမှန်များကို အစားထိုးပါ
JOIN_CHANNEL_URL = "https://t.me/FlickZoneMyanmar"      # မိမိ Channel Link ထည့်ပါ
MOVIE_CHANNEL_URL = "https://t.me/+pV13D8TnhDoxOTQ1"     # မိမိ Movie Channel Link ထည့်ပါ

# BotFather တွင် တွေ့ရသော Bot Username အမှန်
BOT_USERNAME = "@FlickZoneOfficial_bot"

# ရုပ်ရှင်အချက်အလက်များ သိမ်းဆည်းရန် Database
MOVIES_DB = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        movie_id = args[0]
        if movie_id in MOVIES_DB:
            movie = MOVIES_DB[movie_id]
            disclaimer = "\n\n⚠️ သတိပြုရန် - ဤဇာတ်ကားဖိုင်သည် ၅ မိနစ်အတွင်း အလိုအလျောက် ပျက်သွားမည် ဖြစ်ပါသည်။ ပျောက်ဆုံးသွားခြင်း မရှိစေရန်အတွက် မိမိ၏ 'Saved Messages' တွင် သိမ်းထားပေးပါခင်ဗျာ။"
            
            caption = (
                f"🎬 **{movie['title']}**\n\n"
                f"🏷 **Genre:** {movie['genre']}\n\n"
                f"📖 **Synopsis:** {movie['synopsis']}"
                f"{disclaimer}"
            )
            
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/FlickZoneMyanmar")],
                [InlineKeyboardButton("🎬 Movie Channel", url="https://t.me/+pV13D8TnhDoxOTQ1")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            sent_message = await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=movie['file_id'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            # ၅ မိနစ် (၃၀၀ စက္ကန့်) ပြီးလျှင် အလိုအလျောက် ဖျက်မည့် စနစ်
            async def delete_later():
                await asyncio.sleep(300)
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sent_message.message_id)
                except Exception as e:
                    logger.error(f"Error deleting message: {e}")
            
            asyncio.create_task(delete_later())
            return
        else:
            await update.message.reply_text("❌ ရှာမတွေ့ပါ သို့မဟုတ် ဇာတ်ကားလင့်ခ် သက်တမ်းကုန်သွားပါပြီ။")
            return

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/FlickZoneMyanmar")],
        [InlineKeyboardButton("🎬 Movie Channel", url="https://t.me/+pV13D8TnhDoxOTQ1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "မင်္ဂလာပါခင်ဗျာ! FlickZone Movie Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "ဤဘော့တ်မှတစ်ဆင့် ရုပ်ရှင်နှင့် ဇာတ်ကားများကို ရှာဖွေကြည့်ရှုနိုင်ပါသည်။"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    reply_message = message.reply_to_message

    if not reply_message:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင်ကို Reply လုပ်ပြီး /publish မိန့်ခွန်းကို ပို့ပေးပါ။")
        return

    video = reply_message.video or reply_message.document
    if not video:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ ဗီဒီယို သို့မဟုတ် ဖိုင်ကိုသာ Reply လုပ်ပေးပါ။")
        return

    args = context.args
    if not args or "|" not in " ".join(args):
        await update.message.reply_text(
            "❌ ပုံစံမမှန်ပါ။ ဤကဲ့သို့ ပို့ပေးပါ:\n"
            "/publish Movie_1 | Title | Genre | Synopsis"
        )
        return

    text_data = " ".join(args)
    parts = [p.strip() for p in text_data.split("|")]
    
    movie_id = parts[0]
    title = parts[1] if len(parts) > 1 else "Movie Title"
    genre = parts[2] if len(parts) > 2 else "Action"
    synopsis = parts[3] if len(parts) > 3 else "ဇာတ်လမ်းအကျဉ်း..."
    video_file_id = video.file_id

    MOVIES_DB[movie_id] = {
        "title": title,
        "genre": genre,
        "synopsis": synopsis,
        "file_id": video_file_id
    }

    deep_link = f"https://t.me/FlickZoneOfficial_bot?start={movie_id}"


    await update.message.reply_text(
        f"✅ ဇာတ်ကား အောင်မြင်စွာ တင်ပြီးပါပြီ!\n\n"
        f"🔗 **Deep Link:** {deep_link}",
        parse_mode="Markdown"
    )

def main():
    if BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"
        logger.error("BOT_TOKEN environment variable not found!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("publish", publish))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
