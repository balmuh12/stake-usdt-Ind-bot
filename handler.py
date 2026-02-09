from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import add_user_transaction, update_status, get_pending_transactions
from config import PACKAGES, ADMINS

# Menu investasi
async def investment_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Basic", callback_data="invest_Basic")],
        [InlineKeyboardButton("Premium", callback_data="invest_Premium")],
        [InlineKeyboardButton("VIP", callback_data="invest_VIP")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "💼 Pilih Paket Investasi:", reply_markup=reply_markup
    )

# Pilih paket
async def invest_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    name = query.from_user.full_name
    package = query.data.split("_")[1]
    deposit = PACKAGES[package]["min_deposit"]

    added = add_user_transaction(user_id, name, package, deposit)
    if added:
        await query.edit_message_text(
            f"✅ Transaksi dicatat!\nPaket: {package}\nDeposit: Rp {deposit}\nStatus: Pending approval."
        )
    else:
        await query.edit_message_text("⚠️ Kamu sudah memiliki transaksi pending.")

# Admin: lihat pending
async def admin_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ Kamu bukan admin.")
        return

    pending = get_pending_transactions()
    if not pending:
        await update.message.reply_text("✅ Tidak ada transaksi pending.")
        return

    text = "📋 Pending Transactions:\n"
    for u in pending:
        text += f"- {u['name']} | Paket: {u['package']} | Deposit: Rp {u['deposit']}\n"
    await update.message.reply_text(text)

# Admin: approve transaksi
async def admin_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ Kamu bukan admin.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Gunakan: /approve <user_id>")
        return

    target_id = int(context.args[0])
    update_status(target_id, "approved")
    await update.message.reply_text(f"✅ Transaksi {target_id} disetujui.")
