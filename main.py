
import os
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

user_wallets = {}

MIN_DEPOSIT = 15
MIN_WITHDRAW = 10

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ['/balance', '/deposit'],
        ['/spin', '/withdraw']
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_wallets.setdefault(user_id, 0)
    await update.message.reply_text(
        "Welcome to Spin & Win Bot 🎰!\nUse the buttons below to play.",
        reply_markup=get_main_keyboard()
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_wallets.get(user_id, 0)
    await update.message.reply_text(f"💰 Your balance is Rs. {balance}")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📥 To deposit, send Rs. {MIN_DEPOSIT}+ to eSewa/Khalti ID 98xxxxxxx.\nThen send /confirm_deposit after payment."
    )

async def confirm_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_wallets[user_id] = user_wallets.get(user_id, 0) + MIN_DEPOSIT
    await update.message.reply_text("✅ Rs. 15 deposited to your wallet!")

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_wallets.get(user_id, 0)
    if balance < 5:
        await update.message.reply_text("❌ Not enough balance to spin (Rs. 5 needed).")
        return
    user_wallets[user_id] -= 5
    if random.random() < 0.5:
        user_wallets[user_id] += 10
        await update.message.reply_text("🎉 You won Rs. 10!")
    else:
        await update.message.reply_text("😢 You lost this time. Try again!")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_wallets.get(user_id, 0)
    if balance < MIN_WITHDRAW:
        await update.message.reply_text(f"❌ Minimum Rs. {MIN_WITHDRAW} required to withdraw.")
        return
    await update.message.reply_text(f"📤 Send your eSewa/Khalti number to admin for Rs. {balance} withdrawal. Admin will process it shortly.")
    user_wallets[user_id] = 0

TOKEN = os.environ.get("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("deposit", deposit))
app.add_handler(CommandHandler("confirm_deposit", confirm_deposit))
app.add_handler(CommandHandler("spin", spin))
app.add_handler(CommandHandler("withdraw", withdraw))

print("Bot is running...")
app.run_polling()
