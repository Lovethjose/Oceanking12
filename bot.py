import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Bot configuration
BOT_TOKEN = "7620063665:AAG7gILchANNIdtSw4SVvg9272z0PE1hJME"
CHANNEL_LINK = "https://t.me/Oceanking_OCK"
NEWS_CHANNEL_LINK = "https://t.me/Oceannewskin"

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Task structure
TASKS = [
    {
        "id": "join_channel",
        "description": f"Join Telegram Channel: {CHANNEL_LINK}",
        "button": "✅ Verify Channel Join"
    },
    {
        "id": "join_news",
        "description": f"Join News Channel: {NEWS_CHANNEL_LINK}",
        "button": "✅ Verify News Join"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with task instructions"""
    user = update.effective_user
    welcome_msg = (
        f"👋 Hello {user.mention_html()}!\n"
        "🌟 Complete these tasks to qualify for the Oceanking airdrop:\n\n"
    )
    
    # Add task descriptions
    for task in TASKS:
        welcome_msg += f"• {task['description']}\n"
    
    # Create task verification buttons
    keyboard = [
        [InlineKeyboardButton(task["button"], callback_data=task["id"])]
        for task in TASKS
    ]
    
    await update.message.reply_html(
        text=welcome_msg,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_task_completion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process task verification buttons"""
    query = update.callback_query
    user_data = context.user_data
    
    # Initialize completion tracker
    if 'completed_tasks' not in user_data:
        user_data['completed_tasks'] = set()
    
    # Mark task as completed
    user_data['completed_tasks'].add(query.data)
    await query.answer(f"Task verified! {len(user_data['completed_tasks']}/{len(TASKS)} completed")
    
    # Check if all tasks are completed
    if len(user_data['completed_tasks']) == len(TASKS):
        await query.edit_message_text(
            "🎉 Congratulations! You passed the Oceanking airdrop verification!\n\n"
            "Your wallet is now eligible for tokens. Stay tuned for distribution updates!",
            reply_markup=None
        )
    else:
        # Update message with remaining tasks
        remaining = [t for t in TASKS if t['id'] not in user_data['completed_tasks']]
        new_msg = "📝 Remaining tasks:\n\n"
        new_msg += "\n".join(f"• {task['description']}" for task in remaining)
        
        keyboard = [
            [InlineKeyboardButton(task["button"], callback_data=task["id"])] 
            for task in remaining
        ]
        
        await query.edit_message_text(
            text=new_msg,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main() -> None:
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_task_completion))
    
    # Start bot
    application.run_polling()
    logging.info("Bot is now running...")

if __name__ == "__main__":
    main()
