import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ရုပ်ရှင်အချက်အလက်များကို သိမ်းဆည်းရန် ယာယီ Dictionary (Database သဖွယ် အသုံးပြုရန်)
MOVIES_DB = {}

# /start command handler (Deep Linking support အပါအဝင်)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        movie_id = args[0]
        if movie_id in MOVIES_DB:
            movie = MOVIES_DB[movie_id]
            disclaimer = "\n\n⚠️ သတိပြုရန် - ဤဇာတ်ကားဖိုင်သည် ၅ မိနစ်အတွင်း အလိုအလျောက် ပျက်သွားမည် ဖြစ်ပါသည်။ ပျောက်ဆုံးသွားခြင်း မရှိစေရန်အတွက် မိမိ၏ 'Saved Messages' တွင် သိမ်းထားပေးပါခင်ဗျာ。"
            
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
            
            # ဗီဒီယိုဖိုင်နှင့် ပုံ (သို့) ဗီဒီယို သီးသန့် ပို့ခြင်း
            sent_message = await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=movie['file_id'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            # ၅ မိနစ် (၃၀၀ စက္ကန့်) ပြီးလျှင် အလိုအလျောက် ဖျက်မည့် Task
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

# /publish command handler (Admin များအတွက် ဇာတ်ကားတင်ရန်)
async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    reply_message = message.reply_to_message

    if not reply_message or not reply_message.video:
        await update.message.reply_text(
            "ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင်ကို Reply လုပ်ပြီး အောက်ပါ ပုံစံအတိုင်း ပို့ပေးပါ:\n"
            "/publish Movie_ID | Title | Genre | Synopsis"
        )
        return

    args = context.args
    if not args or "|" not in " ".join(args):
        await update.message.reply_text(
            "ပုံစံမမှန်ပါ။ ဤကဲ့သို့ ပို့ပေးပါ:\n"
            "/publish movie123 | Title | Genre | Synopsis"
        )
        return

    text_data = " ".join(args)
    parts = [p.strip() for p in text_data.split("|")]
    
    movie_id = parts[0]
    title = parts[1] if len(parts) > 1 else "Movie Title"
    genre = parts[2] if len(parts) > 2 else "Action"
    synopsis = parts[3] if len(parts) > 3 else "ဇာတ်လမ်းအကျဉ်း..."
    video_file_id = reply_message.video.file_id

    # ဇာတ်ကားအချက်အလက်များကို Database ထဲ သိမ်းဆည်းမည်
    MOVIES_DB[movie_id] = {
        "title": title,
        "genre": genre,
        "synopsis": synopsis,
        "file_id": video_file_id
    }

    bot_username = context.bot.username
    deep_link = f"https://t.me/{bot_username}?start={movie_id}"

    await update.message.reply_text(
        f"✅ ဇာတ်ကား အောင်မြင်စွာ တင်ပြီးပါပြီ!\n\n"
        f"🔗 **Deep Link:** {deep_link}",
        parse_mode="Markdown"
    )

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

