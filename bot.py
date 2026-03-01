import os
import logging
import json
import hashlib
import re
from datetime import datetime, timedelta
from telegram import Update, Document, PhotoSize
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token and admin group link from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_LINK = os.getenv('ADMIN_GROUP_LINK')

# Extract group ID from link or use direct ID
ADMIN_GROUP_ID = None
if ADMIN_GROUP_LINK:
    # Extract group ID from invite link or direct ID
    # Support formats: https://t.me/joinchat/..., https://t.me/..., or direct numeric ID
    if '/joinchat/' in ADMIN_GROUP_LINK:
        # Extract from invite link
        match = re.search(r'/joinchat/([^/]+)', ADMIN_GROUP_LINK)
        if match:
            # For invite links, we'll need to handle this differently
            # For now, we'll store the invite link and use it when needed
            pass
    elif 't.me/' in ADMIN_GROUP_LINK:
        # Extract from public group link
        match = re.search(r't\.me/([^/]+)', ADMIN_GROUP_LINK)
        if match:
            # For public groups, we can use the username
            pass
    else:
        # Assume it's a direct numeric ID
        try:
            ADMIN_GROUP_ID = int(ADMIN_GROUP_LINK.strip('-'))
        except ValueError:
            logger.warning(f"Invalid group ID format: {ADMIN_GROUP_LINK}")

# Admin authentication data file
ADMIN_DATA_FILE = 'admin_data.json'

# Group configuration file
GROUP_CONFIG_FILE = 'group_config.json'

# Conversation states
LOGIN_USERNAME, LOGIN_PASSWORD = range(2)
REGISTER_USERNAME, REGISTER_PASSWORD, CONFIRM_PASSWORD = range(3)
SET_GROUP_LINK = range(1)

# Supported file types
SUPPORTED_DOCUMENT_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']
SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

# Session management
authenticated_admins = {}  # {user_id: {'username': str, 'login_time': datetime}}

def load_group_config():
    """Load group configuration from file"""
    try:
        if os.path.exists(GROUP_CONFIG_FILE):
            with open(GROUP_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading group config: {e}")
    return {'group_link': None}

def save_group_config(data):
    """Save group configuration to file"""
    try:
        with open(GROUP_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving group config: {e}")

def load_admin_data():
    """Load admin data from file"""
    try:
        if os.path.exists(ADMIN_DATA_FILE):
            with open(ADMIN_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading admin data: {e}")
    return {'admins': {}}

def save_admin_data(data):
    """Save admin data to file"""
    try:
        with open(ADMIN_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving admin data: {e}")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_authenticated(user_id):
    """Check if user is authenticated admin"""
    if user_id not in authenticated_admins:
        return False
    
    # Check if session is still valid (24 hours)
    login_time = authenticated_admins[user_id]['login_time']
    if datetime.now() - login_time > timedelta(hours=24):
        del authenticated_admins[user_id]
        return False
    
    return True

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    admin_data = load_admin_data()
    admins = admin_data.get('admins', {})
    
    if username in admins:
        hashed_password = hash_password(password)
        if admins[username]['password'] == hashed_password:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user_id = update.message.from_user.id
    
    if is_authenticated(user_id):
        await update.message.reply_text(
            "👋 Assalomu alaykum, admin! Botga xush kelibsiz.\n\n"
            "Fayl yuborish uchun to'g'ridan-to'g'ri faylni yuboring.\n\n"
            "Admin buyruqlari:\n"
            "/setgroup - Guruh linkini o'rnatish\n"
            "/logout - Tizimdan chiqish\n"
            "/status - Admin holatini ko'rish"
        )
    else:
        await update.message.reply_text(
            "Assalomu alaykum! Men fayl yuborish botiman.\n\n"
            "Quyidagi fayl turlarini yuborishingiz mumkin:\n"
            "📄 PDF fayllar\n"
            "📝 Word hujjatlari (.doc, .docx)\n"
            "🖼️ Rasmlar (JPG, PNG, GIF, WebP)\n\n"
            "Faylni shu yerga yuboring, men uni admin guruhiga yuboraman.\n\n"
            "❌ Ovozli xabarlar va stikerlar qabul qilinmaydi!"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    user_id = update.message.from_user.id
    
    if is_authenticated(user_id):
        help_text = (
            "🔧 Admin yordam:\n\n"
            "Foydalanish uchun:\n"
            "1. PDF, Word yoki rasm faylini yuboring\n"
            "2. Bot faylni avtomatik ravishda admin guruhiga yuboradi\n\n"
            "Admin buyruqlari:\n"
            "/setgroup - Guruh linkini o'rnatish\n"
            "/logout - Tizimdan chiqish\n"
            "/status - Admin holatini ko'rish\n\n"
            "Qo'llab-quvvatlanadigan formatlar:\n"
            "• PDF (.pdf)\n"
            "• Word (.doc, .docx)\n"
            "• Rasmlar (.jpg, .png, .gif, .webp)\n\n"
            "❌ Ovozli xabarlar va stikerlar qabul qilinmaydi!"
        )
    else:
        help_text = (
            "Yordam:\n\n"
            "Foydalanish uchun:\n"
            "1. PDF, Word yoki rasm faylini yuboring\n"
            "2. Bot faylni avtomatik ravishda admin guruhiga yuboradi\n\n"
            "Qo'llab-quvvatlanadigan formatlar:\n"
            "• PDF (.pdf)\n"
            "• Word (.doc, .docx)\n"
            "• Rasmlar (.jpg, .png, .gif, .webp)\n\n"
            "❌ Ovozli xabarlar va stikerlar qabul qilinmaydi!\n\n"
            "Agar admin bo'lsangiz:\n"
            "/login - Admin tizimiga kirish\n"
            "/register - Ro'yxatdan o'tish"
        )
    
    await update.message.reply_text(help_text)

async def get_group_chat_id(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Get group chat ID from link or return direct ID"""
    # First try to get from config file
    group_config = load_group_config()
    group_link = group_config.get('group_link')
    
    if not group_link:
        # Fallback to environment variable
        group_link = ADMIN_GROUP_LINK
    
    if not group_link:
        return None
    
    # If we have a direct ID
    try:
        direct_id = int(group_link.strip('-'))
        return direct_id
    except ValueError:
        pass
    
    # If we have a public group link, try to get chat ID
    if 't.me/' in group_link and '/joinchat/' not in group_link:
        match = re.search(r't\.me/([^/]+)', group_link)
        if match:
            group_username = match.group(1)
            try:
                # Try to get chat info using the username
                chat = await context.bot.get_chat(f"@{group_username}")
                return chat.id
            except Exception as e:
                logger.error(f"Error getting chat info for @{group_username}: {e}")
    
    # For invite links, we need to handle them differently
    # Telegram Bot API doesn't directly support invite links
    # We'll need to extract the chat ID from the invite link or use a different approach
    if '/joinchat/' in group_link or '+' in group_link:
        logger.warning("Invite links are not directly supported. Please use public group link or chat ID.")
        return None
    
    return None

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document files"""
    # Get target group ID
    target_group_id = await get_group_chat_id(context)
    if not target_group_id:
        await update.message.reply_text(
            "❌ Admin guruhiga ulanishda xatolik. Iltimos, admin bilan bog'laning."
        )
        return
    
    document: Document = update.message.document
    
    # Check if document type is supported
    if document.mime_type in SUPPORTED_DOCUMENT_TYPES:
        try:
            # Forward document to admin group
            await context.bot.forward_message(
                chat_id=target_group_id,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
            
            # Get user info
            user = update.message.from_user
            full_name = user.first_name
            if user.last_name:
                full_name += f" {user.last_name}"
            if user.username:
                full_name += f" (@{user.username})"
            
            await update.message.reply_text(
                "✅ Fayl muvaffaqiyatli admin kanali/guruhiga yuborildi!\n\n"
                f"👤 Ism-familiya: {full_name}\n"
                f"📄 Fayl nomi: {document.file_name}\n"
                f"📊 Hajmi: {document.file_size} bytes\n"
                f"📱 Guruh: {update.message.chat.title if update.message.chat.title else 'Shaxsiy chat'}"
            )
            logger.info(f"Document {document.file_name} forwarded to admin group/channel from user {full_name} ({user.id})")
            
        except Exception as e:
            logger.error(f"Error forwarding document: {e}")
            await update.message.reply_text(
                "❌ Faylni yuborishda xatolik yuz berdi. Iltimos, admin bilan bog'laning."
            )
    else:
        await update.message.reply_text(
            "❌ Ushbu fayl turi qo'llab-quvvatlanmaydi.\n\n"
            "Iltimos, faqat PDF, Word yoki rasm fayllarini yuboring."
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo files"""
    # Get target group ID
    target_group_id = await get_group_chat_id(context)
    if not target_group_id:
        await update.message.reply_text(
            "❌ Admin guruhiga ulanishda xatolik. Iltimos, admin bilan bog'laning."
        )
        return
    
    photo: PhotoSize = update.message.photo[-1]  # Get the largest photo
    
    try:
        # Forward photo to admin group
        await context.bot.forward_message(
            chat_id=target_group_id,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        
        # Get user info
        user = update.message.from_user
        full_name = user.first_name
        if user.last_name:
            full_name += f" {user.last_name}"
        if user.username:
            full_name += f" (@{user.username})"
        
        await update.message.reply_text(
            f"✅ Rasm muvaffaqiyatli admin kanali/guruhiga yuborildi!\n\n"
            f"👤 Ism-familiya: {full_name}\n"
            f"📱 Guruh: {update.message.chat.title if update.message.chat.title else 'Shaxsiy chat'}"
        )
        logger.info(f"Photo forwarded to admin group/channel from user {full_name} ({user.id})")
        
    except Exception as e:
        logger.error(f"Error forwarding photo: {e}")
        await update.message.reply_text(
            "❌ Raslni yuborishda xatolik yuz berdi. Iltimos, admin bilan bog'laning."
        )

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle other message types"""
    # Check for blocked content types
    if update.message.voice:
        await update.message.reply_text(
            "❌ Ovozli xabarlar qabul qilinmaydi!\n\n"
            "Iltimos, faqat PDF, Word yoki rasm fayllarini yuboring."
        )
    elif update.message.sticker:
        await update.message.reply_text(
            "❌ Stikerlar qabul qilinmaydi!\n\n"
            "Iltimos, faqat PDF, Word yoki rasm fayllarini yuboring."
        )
    else:
        await update.message.reply_text(
            "❌ Faqat fayllar qabul qilinadi.\n\n"
            "Iltimos, PDF, Word yoki rasm faylini yuboring.\n\n"
            "❌ Ovozli xabarlar va stikerlar qabul qilinmaydi!"
        )

# Login conversation handlers
async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start login conversation"""
    await update.message.reply_text(
        "🔐 Tizimga kirish\n\n"
        "Iltimos, foydalanuvchi nomingizni kiriting:"
    )
    return LOGIN_USERNAME

async def login_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle username input"""
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Endi parolingizni kiriting:")
    return LOGIN_PASSWORD

async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input and authenticate"""
    username = context.user_data['username']
    password = update.message.text
    
    if authenticate_user(username, password):
        user_id = update.message.from_user.id
        authenticated_admins[user_id] = {
            'username': username,
            'login_time': datetime.now()
        }
        
        await update.message.reply_text(
            f"✅ Tizimga muvaffaqiyatli kirdingiz, {username}!\n\n"
            "Endi fayllarni yuborishingiz mumkin."
        )
        logger.info(f"Admin {username} logged in successfully")
    else:
        await update.message.reply_text(
            "❌ Foydalanuvchi nomi yoki parol noto'g'ri!\n\n"
            "Qayta urinib ko'ring: /login"
        )
    
    return ConversationHandler.END

# Register conversation handlers
async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start registration conversation"""
    await update.message.reply_text(
        "📝 Ro'yxatdan o'tish\n\n"
        "Iltimos, yangi foydalanuvchi nomini kiriting:"
    )
    return REGISTER_USERNAME

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle username input for registration"""
    username = update.message.text
    
    # Check if username already exists
    admin_data = load_admin_data()
    if username in admin_data.get('admins', {}):
        await update.message.reply_text(
            "❌ Bu foydalanuvchi nomi allaqachon mavjud!\n\n"
            "Boshqa nom tanlang:"
        )
        return REGISTER_USERNAME
    
    context.user_data['new_username'] = username
    await update.message.reply_text("Parolni kiriting:")
    return REGISTER_PASSWORD

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input for registration"""
    context.user_data['new_password'] = update.message.text
    await update.message.reply_text("Parolni tasdiqlang (qayta kiriting):")
    return CONFIRM_PASSWORD

async def register_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password confirmation and complete registration"""
    password = context.user_data['new_password']
    confirm_password = update.message.text
    username = context.user_data['new_username']
    
    if password != confirm_password:
        await update.message.reply_text(
            "❌ Parollar mos kelmadi!\n\n"
            "Qaytadan urinib ko'ring: /register"
        )
        return ConversationHandler.END
    
    # Save new admin
    admin_data = load_admin_data()
    admin_data.setdefault('admins', {})
    admin_data['admins'][username] = {
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'created_by': update.message.from_user.id
    }
    save_admin_data(admin_data)
    
    await update.message.reply_text(
        f"✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
        f"Foydalanuvchi nomi: {username}\n"
        "Endi tizimga kirishingiz mumkin: /login"
    )
    logger.info(f"New admin registered: {username}")
    
    return ConversationHandler.END

async def set_group_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start set group conversation"""
    user_id = update.message.from_user.id
    
    # Check if user is authenticated admin
    if not is_authenticated(user_id):
        await update.message.reply_text(
            "❌ Bu buyruq faqat adminlar uchun!\n\n"
            "/login - Tizimga kirish"
        )
        return ConversationHandler.END
    
    # Show current group link if exists
    group_config = load_group_config()
    current_link = group_config.get('group_link')
    
    if current_link:
        await update.message.reply_text(
            f"📋 Joriy guruh linki: {current_link}\n\n"
            "Yangi guruh linkini kiriting (masalan: https://t.me/guruh_nomi):"
        )
    else:
        await update.message.reply_text(
            "🔗 Guruh linkini o'rnatish\n\n"
            "Guruh linkini kiriting (masalan: https://t.me/guruh_nomi):"
        )
    
    return SET_GROUP_LINK

async def set_group_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle group link input"""
    user_id = update.message.from_user.id
    new_link = update.message.text.strip()
    
    # Validate link format
    if not new_link or ('t.me/' not in new_link and not new_link.lstrip('-').isdigit()):
        await update.message.reply_text(
            "❌ Noto'g'ri link format!\n\n"
            "To'g'ri formatlar:\n"
            "• https://t.me/guruh_nomi\n"
            "• https://t.me/joinchat/ABC123\n"
            "• -1001234567890\n\n"
            "Qaytadan urinib ko'ring: /setgroup"
        )
        return ConversationHandler.END
    
    # Save new group link
    group_config = load_group_config()
    group_config['group_link'] = new_link
    save_group_config(group_config)
    
    await update.message.reply_text(
        f"✅ Guruh linki muvaffaqiyatli o'rnatildi!\n\n"
        f"Yangi link: {new_link}\n"
        f"O'rnatgan admin: {authenticated_admins[user_id]['username']}"
    )
    logger.info(f"Group link updated to {new_link} by admin {authenticated_admins[user_id]['username']}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation"""
    await update.message.reply_text("❌ Amal bekor qilindi.")
    return ConversationHandler.END

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle logout command"""
    user_id = update.message.from_user.id
    
    if user_id in authenticated_admins:
        username = authenticated_admins[user_id]['username']
        del authenticated_admins[user_id]
        await update.message.reply_text(
            f"👋 Tizimdan muvaffaqiyatli chiqdingiz, {username}!"
        )
        logger.info(f"Admin {username} logged out")
    else:
        await update.message.reply_text(
            "❌ Siz tizimga kirishmagan ekansiz."
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle status command"""
    user_id = update.message.from_user.id
    
    if is_authenticated(user_id):
        username = authenticated_admins[user_id]['username']
        login_time = authenticated_admins[user_id]['login_time']
        
        # Get current group config
        group_config = load_group_config()
        group_link = group_config.get('group_link', "O'rnatilmagan")
        
        await update.message.reply_text(
            f"👤 Admin holati:\n\n"
            f"Foydalanuvchi: {username}\n"
            f"Tizimga kirish vaqti: {login_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Holat: ✅ Faol\n\n"
            f"🔗 Guruh linki: {group_link}"
        )
    else:
        await update.message.reply_text(
            "❌ Siz tizimga kirishmagan ekansiz.\n\n"
            "/login - Tizimga kirish"
        )

def main() -> None:
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Create conversation handlers
    login_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login_start)],
        states={
            LOGIN_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_username)],
            LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    register_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register_start)],
        states={
            REGISTER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
            CONFIRM_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    setgroup_handler = ConversationHandler(
        entry_points=[CommandHandler('setgroup', set_group_start)],
        states={
            SET_GROUP_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_group_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(login_handler)
    application.add_handler(register_handler)
    application.add_handler(setgroup_handler)
    
    # Add document handler for PDF and Word files
    application.add_handler(
        MessageHandler(
            filters.Document.ALL & (
                filters.Document.FileExtension("pdf") |
                filters.Document.FileExtension("doc") |
                filters.Document.FileExtension("docx")
            ),
            handle_document
        )
    )
    
    # Add photo handler
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Add handler for blocked content (voice, sticker) and other messages
    application.add_handler(
        MessageHandler(
            filters.VOICE | filters.Sticker.ALL | filters.TEXT | filters.VIDEO | filters.AUDIO,
            handle_other_messages
        )
    )
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling()

if __name__ == '__main__':
    main()
