import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers import investment_menu, invest_callback, admin_pending, admin_approve

TOKEN = os.environ.get("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# Command
app.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Selamat datang di Stake USDT SG!")))
app.add_handler(CommandHandler("pending", admin_pending))
app.add_handler(CommandHandler("approve", admin_approve))

# Callback menu investasi
app.add_handler(CallbackQueryHandler(investment_menu, pattern="^investment$"))
app.add_handler(CallbackQueryHandler(invest_callback, pattern="^invest_"))

# Jalankan bot
app.run_polling()
