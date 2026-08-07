import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ခနလေးစောင့်ပါ၊ စစ်ဆေးနေပါတယ်...")
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်ုပ်သည် သင့်ရဲ့ Bot ဖြစ်ပါသည်။ အဆင်သင့် ဖြစ်ပါပြီ။")

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN", "8669551565:AAH2NvjXyHWL-C13vakXwpzjg6t9R8_grvg")
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    print("Bot is running...")
    application.run_polling()
  
