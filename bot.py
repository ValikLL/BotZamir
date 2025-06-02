import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import datetime
import json
import os

# Bot token
BOT_TOKEN = "8030196883:AAFW9Z-leI9SFwkaA27DoXmvdfTlArWlrsM"

# Initial admin ID
ADMIN_ID = 333688384

# File to store data
DATA_FILE = "data.json"

# Localization dictionary
translations = {
    "uk": {
        "welcome": "👋 Вітаємо в Tochniy Zamir! Оберіть опцію:",
        "create_order": "📝 Створити Замовлення",
        "personal_cabinet": "👤 Особистий Кабінет",
        "admin_menu": "🔧 Адмін-Панель Tochniy Zamir",
        "new_orders": "📋 Нові Замовлення",
        "processed_orders": "✅ Оброблені Замовлення",
        "client_list": "👥 Список Клієнтів",
        "remove_booking": "🗓 Зняти Бронювання",
        "list_admins": "👮 Переглянути Адміністраторів",
        "main_menu": "🏠 Головне Меню",
        "access_denied": "❌ Доступ заборонено! Ви не адміністратор.",
        "enter_name": "📝 Введіть ваше ім’я:",
        "empty_name": "⚠️ Ім’я не може бути порожнім. Введіть ім’я!",
        "enter_phone": "📞 Введіть номер телефону або поділіться контактом:",
        "share_phone": "📞 Поділитися номером",
        "empty_phone": "⚠️ Номер не може бути порожнім. Введіть номер телефону!",
        "enter_description": "📋 Опишіть, що потрібно зробити (який замір):",
        "empty_description": "⚠️ Опис не може бути порожним. Опишіть, що потрібно зробити!",
        "send_photo": "📸 Надішліть фото об’єкта:",
        "photo_required": "⚠️ Будь ласка, надішліть фото!",
        "enter_address": "📍 Введіть місто, вулицю та номер будинку:",
        "empty_address": "⚠️ Адреса не може бути порожньою. Введіть місто, вулицю та номер будинку!",
        "select_date": "🗓 Оберіть дату для заміру:",
        "select_time": "⏰ Оберіть час для заміру:",
        "order_created": "✅ Замовлення створено!\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📋 Опис: {description}\n📍 Адреса: {address}\n🗓 Дата та час: {date} {time}",
        "new_order_notification": "📋 Нове замовлення!\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📋 Опис: {description}\n📍 Адреса: {address}\n🗓 Дата та час: {date} {time}",
        "return_to_main": "Поверніться до головного меню:",
        "error": "⚠️ Щось пішло не так. Спробуйте ще раз з /start!",
        "no_orders": "📂 У вас немає замовлень.",
        "order_info": "📋 Замовлення\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📋 Опис: {description}\n📍 Адреса: {address}\n🗓 Дата та час: {date} {time}\n📊 Статус: {status}",
        "processed": "✅ Оброблено",
        "not_processed": "⏳ Не оброблено",
        "no_new_orders": "📂 Немає нових замовлень.",
        "no_processed_orders": "📂 Немає оброблених замовлень.",
        "order_processed": "✅ Замовлення від {name} оброблено!",
        "no_clients": "📂 Немає клієнтів.",
        "client": "Клієнт: {name}",
        "no_bookings": "📂 Немає активних бронювань.",
        "select_booking": "🗓 Оберіть бронювання для видалення:",
        "booking_removed": "🗑 Бронювання {slot} для {name} успішно знято!",
        "booking_not_found": "⚠️ Бронювання {slot} не знайдено.",
        "change_language": "🌐 Змінити мову",
        "select_language": "🌐 Оберіть мову:",
        "language_changed": "✅ Мову змінено на {language}!",
        "back": "⬅️ Назад",
        "previous": "⬅️ Попередній",
        "next": "Наступний ➡️",
        "list_admins_title": "👮 Список адміністраторів",
        "admin_info": "Адміністратор: {name} (ID: {id})",
        "edit_client_name": "✏️ Змінити ім'я клієнта",
        "enter_new_client_name": "✏️ Введіть нове ім'я для клієнта (видиме лише адміну):",
        "client_name_updated": "✅ Ім'я клієнта оновлено до: {name}",
        "create_another_order": "📝 Створити ще замовлення",
        "add_admin": "➕ Додати адміністратора",
        "enter_admin_id": "👮 Введіть Telegram ID нового адміністратора:",
        "enter_admin_name": "📝 Введіть ім'я нового адміністратора:",
        "admin_added": "✅ Адміністратора {name} (ID: {id}) додано!",
        "invalid_admin_id": "⚠️ Некоректний Telegram ID. Введіть числовий ID.",
        "remove_admin": "🗑 Видалити",
        "admin_removed": "✅ Адміністратора {name} (ID: {id}) видалено!",
        "cannot_remove_main_admin": "⚠️ Неможливо видалити основного адміністратора!",
        "personal_cabinet_info": "👤 Особистий Кабінет\n📝 Ім'я: {name}\n📞 Телефон: {phone}\n📊 Замовлень: {order_count}\n📅 Дата реєстрації: {registration_date}",
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в Tochniy Zamir! Выберите опцию:",
        "create_order": "📝 Создать Заказ",
        "personal_cabinet": "👤 Личный Кабинет",
        "admin_menu": "🔧 Панель Администратора Tochniy Zamir",
        "new_orders": "📋 Новые Заказы",
        "processed_orders": "✅ Обработанные Заказы",
        "client_list": "👥 Список Клиентов",
        "remove_booking": "🗓 Снять Бронирование",
        "list_admins": "👮 Просмотреть Администраторов",
        "main_menu": "🏠 Главное Меню",
        "access_denied": "❌ Доступ запрещён! Вы не администратор.",
        "enter_name": "📝 Введите ваше имя:",
        "empty_name": "⚠️ Имя не может быть пустым. Введите имя!",
        "enter_phone": "📞 Введите номер телефона или поделитесь контактом:",
        "share_phone": "📞 Поделиться номером",
        "empty_phone": "⚠️ Номер не может быть пустым. Введите номер телефона!",
        "enter_description": "📋 Опишите, что нужно сделать (какой замер):",
        "empty_description": "⚠️ Описание не может быть пустым. Опишите, что нужно сделать!",
        "send_photo": "📸 Отправьте фото объекта:",
        "photo_required": "⚠️ Пожалуйста, отправьте фото!",
        "enter_address": "📍 Введите город, улицу и номер дома:",
        "empty_address": "⚠️ Адрес не может быть пустым. Введите город, улицу и номер дома!",
        "select_date": "🗓 Выберите дату для замера:",
        "select_time": "⏰ Выберите время для замера:",
        "order_created": "✅ Заказ создан!\n👤 Имя: {name}\n📞 Телефон: {phone}\n📋 Описание: {description}\n📍 Адрес: {address}\n🗓 Дата и время: {date} {time}",
        "new_order_notification": "📋 Новый заказ!\n👤 Имя: {name}\n📞 Телефон: {phone}\n📋 Описание: {description}\n📍 Адрес: {address}\n🗓 Дата и время: {date} {time}",
        "return_to_main": "Вернитесь в главное меню:",
        "error": "⚠️ Что-то пошло не так. Попробуйте снова с /start!",
        "no_orders": "📂 У вас нет заказов.",
        "order_info": "📋 Заказ\n👤 Имя: {name}\n📞 Телефон: {phone}\n📋 Описание: {description}\n📍 Адрес: {address}\n🗓 Дата и время: {date} {time}\n📊 Статус: {status}",
        "processed": "✅ Обработан",
        "not_processed": "⏳ Не обработан",
        "no_new_orders": "📂 Нет новых заказов.",
        "no_processed_orders": "📂 Нет обработанных заказов.",
        "order_processed": "✅ Заказ от {name} обработан!",
        "no_clients": "📂 Нет клиентов.",
        "client": "Клиент: {name}",
        "no_bookings": "📂 Нет активных бронирований.",
        "select_booking": "🗓 Выберите бронирование для удаления:",
        "booking_removed": "🗑 Бронирование {slot} для {name} успешно снято!",
        "booking_not_found": "⚠️ Бронирование {slot} не найдено.",
        "change_language": "🌐 Изменить язык",
        "select_language": "🌐 Выберите язык:",
        "language_changed": "✅ Язык изменён на {language}!",
        "back": "⬅️ Назад",
        "previous": "⬅️ Предыдущий",
        "next": "Следующий ➡️",
        "list_admins_title": "👮 Список администраторов",
        "admin_info": "Администратор: {name} (ID: {id})",
        "edit_client_name": "✏️ Изменить имя клиента",
        "enter_new_client_name": "✏️ Введите новое имя для клиента (видимое только админу):",
        "client_name_updated": "✅ Имя клиента обновлено до: {name}",
        "create_another_order": "📝 Создать ещё заказ",
        "add_admin": "➕ Добавить администратора",
        "enter_admin_id": "👮 Введите Telegram ID нового администратора:",
        "enter_admin_name": "📝 Введите имя нового администратора:",
        "admin_added": "✅ Администратора {name} (ID: {id}) добавлено!",
        "invalid_admin_id": "⚠️ Некорректный Telegram ID. Введите числовой ID.",
        "remove_admin": "🗑 Удалить",
        "admin_removed": "✅ Администратора {name} (ID: {id}) удалено!",
        "cannot_remove_main_admin": "⚠️ Нельзя удалить основного администратора!",
        "personal_cabinet_info": "👤 Личный Кабинет\n📝 Имя: {name}\n📞 Телефон: {phone}\n📊 Заказов: {order_count}\n📅 Дата регистрации: {registration_date}",
    },
    "en": {
        "welcome": "👋 Welcome to Tochniy Zamir! Choose an option:",
        "create_order": "📝 Create Order",
        "personal_cabinet": "👤 Personal Cabinet",
        "admin_menu": "🔧 Tochniy Zamir Admin Panel",
        "new_orders": "📋 New Orders",
        "processed_orders": "✅ Processed Orders",
        "client_list": "👥 Client List",
        "remove_booking": "🗓 Remove Booking",
        "list_admins": "👮 View Administrators",
        "main_menu": "🏠 Main Menu",
        "access_denied": "❌ Access denied! You are not an administrator.",
        "enter_name": "📝 Enter your name:",
        "empty_name": "⚠️ Name cannot be empty. Please enter a name!",
        "enter_phone": "📞 Enter your phone number or share your contact:",
        "share_phone": "📞 Share number",
        "empty_phone": "⚠️ Phone number cannot be empty. Please enter a phone number!",
        "enter_description": "📋 Describe what needs to be done (what measurement):",
        "empty_description": "⚠️ Description cannot be empty. Please describe what needs to be done!",
        "send_photo": "📸 Send a photo of the object:",
        "photo_required": "⚠️ Please send a photo!",
        "enter_address": "📍 Enter city, street, and house number:",
        "empty_address": "⚠️ Address cannot be empty. Please enter city, street, and house number!",
        "select_date": "🗓 Choose a date for the measurement:",
        "select_time": "⏰ Choose a time for the measurement:",
        "order_created": "✅ Order created!\n👤 Name: {name}\n📞 Phone: {phone}\n📋 Description: {description}\n📍 Address: {address}\n🗓 Date and time: {date} {time}",
        "new_order_notification": "📋 New order!\n👤 Name: {name}\n📞 Phone: {phone}\n📋 Description: {description}\n📍 Address: {address}\n🗓 Date and time: {date} {time}",
        "return_to_main": "Return to the main menu:",
        "error": "⚠️ Something went wrong. Try again with /start!",
        "no_orders": "📂 You have no orders.",
        "order_info": "📋 Order\n👤 Name: {name}\n📞 Phone: {phone}\n📋 Description: {description}\n📍 Address: {address}\n🗓 Date and time: {date} {time}\n📊 Status: {status}",
        "processed": "✅ Processed",
        "not_processed": "⏳ Not processed",
        "no_new_orders": "📂 No new orders.",
        "no_processed_orders": "📂 No processed orders.",
        "order_processed": "✅ Order from {name} processed!",
        "no_clients": "📂 No clients.",
        "client": "Client: {name}",
        "no_bookings": "📂 No active bookings.",
        "select_booking": "🗓 Choose a booking to remove:",
        "booking_removed": "🗑 Booking {slot} for {name} successfully removed!",
        "booking_not_found": "⚠️ Booking {slot} not found.",
        "change_language": "🌐 Change Language",
        "select_language": "🌐 Select language:",
        "language_changed": "✅ Language changed to {language}!",
        "back": "⬅️ Back",
        "previous": "⬅️ Previous",
        "next": "Next ➡️",
        "list_admins_title": "👮 List of Administrators",
        "admin_info": "Administrator: {name} (ID: {id})",
        "edit_client_name": "✏️ Edit Client Name",
        "enter_new_client_name": "✏️ Enter new name for the client (visible only to admin):",
        "client_name_updated": "✅ Client name updated to: {name}",
        "create_another_order": "📝 Create another order",
        "add_admin": "➕ Add Administrator",
        "enter_admin_id": "👮 Enter Telegram ID of the new administrator:",
        "enter_admin_name": "📝 Enter the name of the new administrator:",
        "admin_added": "✅ Administrator {name} (ID: {id}) added!",
        "invalid_admin_id": "⚠️ Invalid Telegram ID. Please enter a numeric ID.",
        "remove_admin": "🗑 Remove",
        "admin_removed": "✅ Administrator {name} (ID: {id}) removed!",
        "cannot_remove_main_admin": "⚠️ Cannot remove the main administrator!",
        "personal_cabinet_info": "👤 Personal Cabinet\n📝 Name: {name}\n📞 Phone: {phone}\n📊 Orders: {order_count}\n📅 Registration Date: {registration_date}",
    }
}

# Helper function to get translated text
def get_text(key, context, **kwargs):
    lang = context.user_data.get("language", "uk")
    text = translations.get(lang, translations["uk"]).get(key, translations["uk"].get(key, ""))
    return text.format(**kwargs)

# Helper function to get language name
def get_language_name(lang):
    names = {"uk": "Українська", "ru": "Русский", "en": "English"}
    return names.get(lang, "Українська")

# Load data from file
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "admins" not in data:
                    data["admins"] = {str(ADMIN_ID): {"name": "Main Admin"}}
                return data
        return {
            "orders": [],
            "bookings": {},
            "clients": {},
            "admins": {str(ADMIN_ID): {"name": "Main Admin"}}
        }
    except json.JSONDecodeError:
        print("Помилка: Некоректний формат файлу data.json")
        return {
            "orders": [],
            "bookings": {},
            "clients": {},
            "admins": {str(ADMIN_ID): {"name": "Main Admin"}}
        }
    except Exception as e:
        print(f"Помилка при завантаженні файлу: {e}")
        return {
            "orders": [],
            "bookings": {},
            "clients": {},
            "admins": {str(ADMIN_ID): {"name": "Main Admin"}}
        }

# Save data to file
def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Помилка при збереженні файлу: {e}")

# Initialize data
data = load_data()

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Error: {context.error}")
    if update and update.callback_query:
        await update.callback_query.message.reply_text(get_text("error", context))
    elif update and update.message:
        await update.message.reply_text(get_text("error", context))

# Main menu for clients or admins
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.setdefault("language", "uk")
    user_id = str(update.effective_user.id)
    if user_id in data["admins"]:
        await admin(update, context)
    else:
        keyboard = [
            [InlineKeyboardButton(get_text("create_order", context), callback_data="create_order")],
            [InlineKeyboardButton(get_text("personal_cabinet", context), callback_data="personal_cabinet")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text("welcome", context), reply_markup=reply_markup)

# Admin menu
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    if user_id not in data["admins"]:
        if update.message:
            await update.message.reply_text(get_text("access_denied", context))
        elif update.callback_query:
            await update.callback_query.message.reply_text(get_text("access_denied", context))
        return
    keyboard = [
        [InlineKeyboardButton(get_text("new_orders", context), callback_data="new_orders")],
        [InlineKeyboardButton(get_text("processed_orders", context), callback_data="processed_orders")],
        [InlineKeyboardButton(get_text("client_list", context), callback_data="client_list")],
        [InlineKeyboardButton(get_text("remove_booking", context), callback_data="remove_booking")],
        [InlineKeyboardButton(get_text("list_admins", context), callback_data="list_admins")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(get_text("admin_menu", context), reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(get_text("admin_menu", context), reply_markup=reply_markup)

# Create order: Step 1 - Phone
async def create_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data["order"] = {}
    context.user_data["step"] = "phone"
    keyboard = [[KeyboardButton(get_text("share_phone", context), request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await query.message.reply_text(get_text("enter_phone", context), reply_markup=reply_markup)

# Handle text, contact, and photo for order creation
async def handle_order_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get("step")
    order = context.user_data.get("order", {})
    
    if not step:
        await update.message.reply_text(get_text("error", context))
        return

    if step == "phone":
        user_id = str(update.effective_user.id)
        if update.message.contact:
            order["phone"] = update.message.contact.phone_number
            contact_name = update.message.contact.first_name
            if user_id not in data["clients"]:
                if contact_name:
                    data["clients"][user_id] = {
                        "original_name": contact_name,
                        "admin_name": None,
                        "registration_date": datetime.date.today().strftime("%Y-%m-%d")
                    }
                    order["name"] = contact_name
                    save_data(data)
                    context.user_data["step"] = "description"
                    await update.message.reply_text(
                        get_text("enter_description", context),
                        reply_markup=telegram.ReplyKeyboardRemove()
                    )
                else:
                    context.user_data["step"] = "name"
                    await update.message.reply_text(
                        get_text("enter_name", context),
                        reply_markup=telegram.ReplyKeyboardRemove()
                    )
            else:
                order["name"] = data["clients"][user_id]["original_name"]
                context.user_data["step"] = "description"
                await update.message.reply_text(
                    get_text("enter_description", context),
                    reply_markup=telegram.ReplyKeyboardRemove()
                )
        else:
            order["phone"] = update.message.text.strip()
            if not order["phone"]:
                await update.message.reply_text(get_text("empty_phone", context))
                return
            context.user_data["step"] = "name"
            await update.message.reply_text(
                get_text("enter_name", context),
                reply_markup=telegram.ReplyKeyboardRemove()
            )
    elif step == "name":
        name = update.message.text.strip()
        if not name:
            await update.message.reply_text(get_text("empty_name", context))
            return
        user_id = str(update.effective_user.id)
        if user_id not in data["clients"]:
            data["clients"][user_id] = {
                "original_name": name,
                "admin_name": None,
                "registration_date": datetime.date.today().strftime("%Y-%m-%d")
            }
            save_data(data)
        order["name"] = data["clients"][user_id]["original_name"]
        context.user_data["step"] = "description"
        await update.message.reply_text(get_text("enter_description", context))
    elif step == "description":
        order["description"] = update.message.text.strip()
        if not order["description"]:
            await update.message.reply_text(get_text("empty_description", context))
            return
        context.user_data["step"] = "photo"
        await update.message.reply_text(get_text("send_photo", context))
    elif step == "photo" and update.message.photo:
        order["photo"] = update.message.photo[-1].file_id
        context.user_data["step"] = "address"
        await update.message.reply_text(get_text("enter_address", context))
    elif step == "photo":
        await update.message.reply_text(get_text("photo_required", context))
    elif step == "address":
        order["address"] = update.message.text.strip()
        if not order["address"]:
            await update.message.reply_text(get_text("empty_address", context))
            return
        context.user_data["step"] = "date"
        context.user_data["calendar"] = {"year": datetime.date.today().year, "month": datetime.date.today().month}
        await show_calendar(update, context)
    elif step == "add_admin_id":
        admin_id = update.message.text.strip()
        if not admin_id.isdigit():
            await update.message.reply_text(get_text("invalid_admin_id", context))
            return
        context.user_data["new_admin"] = {"id": admin_id}
        context.user_data["step"] = "add_admin_name"
        await update.message.reply_text(get_text("enter_admin_name", context))
    elif step == "add_admin_name":
        admin_name = update.message.text.strip()
        if not admin_name:
            await update.message.reply_text(get_text("empty_name", context))
            return
        admin_id = context.user_data["new_admin"]["id"]
        data["admins"][admin_id] = {"name": admin_name}
        save_data(data)
        await update.message.reply_text(
            get_text("admin_added", context, name=admin_name, id=admin_id)
        )
        context.user_data.pop("step", None)
        context.user_data.pop("new_admin", None)
        await list_admins(update, context)
    elif step == "edit_client_name":
        user_id = context.user_data.get("edit_client_id")
        new_name = update.message.text.strip()
        if not new_name:
            await update.message.reply_text(get_text("empty_name", context))
            return
        if user_id in data["clients"]:
            data["clients"][user_id]["admin_name"] = new_name
            save_data(data)
            await update.message.reply_text(
                get_text("client_name_updated", context, name=new_name)
            )
            context.user_data.pop("step", None)
            context.user_data.pop("edit_client_id", None)
            await view_client_orders(update, context, user_id=user_id)
    else:
        await update.message.reply_text(get_text("error", context))

# Show calendar for date selection
async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    calendar = context.user_data.get("calendar", {"year": datetime.date.today().year, "month": datetime.date.today().month})
    year, month = calendar["year"], calendar["month"]
    today = datetime.date.today()
    
    first_day = datetime.date(year, month, 1)
    days_in_month = (datetime.date(year, month + 1, 1) - datetime.timedelta(days=1) if month < 12 else datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)).day
    keyboard = []
    row = []
    weekday = first_day.weekday()
    for _ in range(weekday):
        row.append(InlineKeyboardButton(" ", callback_data="ignore"))
    for day in range(1, days_in_month + 1):
        date = datetime.date(year, month, day)
        date_str = date.strftime("%Y-%m-%d")
        if date >= today and date_str not in data["bookings"]:
            row.append(InlineKeyboardButton(str(day), callback_data=f"date_{date_str}"))
        else:
            row.append(InlineKeyboardButton("✖️", callback_data="ignore"))
        if len(row) == 7:
            keyboard.append(row)
            row = []
    if row:
        while len(row) < 7:
            row.append(InlineKeyboardButton(" ", callback_data="ignore"))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(get_text("previous", context), callback_data=f"prev_month_{year}_{month}"),
        InlineKeyboardButton(f"🗓 {year}-{month:02d}", callback_data="ignore"),
        InlineKeyboardButton(get_text("next", context), callback_data=f"next_month_{year}_{month}")
    ])
    keyboard.append([InlineKeyboardButton(get_text("back", context), callback_data="back_to_order")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(get_text("select_date", context), reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(get_text("select_date", context), reply_markup=reply_markup)

# Show time slots for selected date
async def show_time_slots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    date = query.data.split("_")[1]
    context.user_data["order"]["date"] = date
    times = ["09:00", "11:00", "13:00", "15:00", "17:00"]
    keyboard = []
    for time in times:
        slot = f"{date}_{time}"
        if slot not in data["bookings"]:
            keyboard.append([InlineKeyboardButton(f"⏰ {time}", callback_data=f"time_{slot}")])
    keyboard.append([InlineKeyboardButton(get_text("back", context), callback_data="back_to_date")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("select_time", context), reply_markup=reply_markup)

# Confirm order and notify admins
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    slot = query.data
    order = context.user_data.get("order", {})
    
    parts = slot.split("_")
    if len(parts) != 3 or parts[0] != "time" or "name" not in order:
        await query.message.reply_text(get_text("error", context))
        return
    
    date, time = parts[1], parts[2]
    order["date"] = date
    order["time"] = time
    order["user_id"] = query.from_user.id
    order["processed"] = False
    data["orders"].append(order)
    data["bookings"][f"{date}_{time}"] = order["name"]
    save_data(data)
    
    await query.message.reply_text(
        get_text("order_created", context,
                 name=order["name"], phone=order["phone"], description=order["description"],
                 address=order["address"], date=order["date"], time=order["time"])
    )
    keyboard = [
        [InlineKeyboardButton(get_text("create_another_order", context), callback_data="create_another_order")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)
    
    for admin_id in data["admins"]:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=get_text("new_order_notification", context,
                              name=order["name"], phone=order["phone"], description=order["description"],
                              address=order["address"], date=order["date"], time=order["time"])
            )
            if "photo" in order:
                try:
                    await context.bot.send_photo(chat_id=admin_id, photo=order["photo"])
                except telegram.error.BadRequest as e:
                    print(f"Помилка при надсиланні фото: {e}")
        except telegram.error.InvalidToken:
            print(f"Помилка: Некоректний токен бота")
        except telegram.error.NetworkError:
            print(f"Помилка мережі при надсиланні повідомлення адміну {admin_id}")
        except Exception as e:
            print(f"Помилка при надсиланні повідомлення адміну {admin_id}: {e}")
    
    # Clean up user data after order confirmation
    context.user_data.pop("order", None)
    context.user_data.pop("step", None)
    context.user_data.pop("calendar", None)

# Personal cabinet
async def personal_cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    client_info = data["clients"].get(user_id, {})
    if not client_info:
        await query.message.reply_text(get_text("no_orders", context))
        return
    
    user_orders = [o for o in data["orders"] if str(o.get("user_id")) == user_id]
    last_phone = user_orders[-1]["phone"] if user_orders else "Невідомо"
    
    await query.message.reply_text(
        get_text("personal_cabinet_info", context,
                 name=client_info.get("original_name", "Невідомо"),
                 phone=last_phone,
                 order_count=len(user_orders),
                 registration_date=client_info.get("registration_date", "Невідомо"))
    )
    
    if user_orders:
        for order in user_orders:
            status = get_text("processed", context) if order.get("processed", False) else get_text("not_processed", context)
            text = get_text(
                "order_info", context,
                name=order["name"],
                phone=order["phone"],
                description=order["description"],
                address=order["address"],
                date=order["date"],
                time=order["time"],
                status=status
            )
            await query.message.reply_text(text)
    
    keyboard = [
        [InlineKeyboardButton(get_text("change_language", context), callback_data="change_language")],
        [InlineKeyboardButton(get_text("back", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Change language menu
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Українська", callback_data="lang_uk")],
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton(get_text("back", context), callback_data="personal_cabinet")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("select_language", context), reply_markup=reply_markup)

# Set language
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    if lang in ["uk", "ru", "en"]:
        context.user_data["language"] = lang
        await query.message.reply_text(
            get_text("language_changed", context, language=get_language_name(lang))
        )
    else:
        await query.message.reply_text(get_text("error", context))
    keyboard = [
        [InlineKeyboardButton(get_text("change_language", context), callback_data="change_language")],
        [InlineKeyboardButton(get_text("back", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: New orders
async def new_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    new_orders = [o for o in data["orders"] if not o.get("processed", False)]
    if not new_orders:
        await query.message.reply_text(get_text("no_new_orders", context))
    else:
        for i, order in enumerate(new_orders):
            name = data["clients"].get(str(order.get("user_id")), {}).get("admin_name") or order.get("name", "unknown")
            text = get_text(
                "order_info", context,
                name=name,
                phone=order.get("phone", "unknown"),
                description=order.get("description", "unknown"),
                address=order.get("address", "unknown"),
                date=order.get("date", "unknown"),
                time=order.get("time", "unknown"),
                status=get_text("not_processed", context)
            )
            await query.message.reply_text(text)
            keyboard = [
                [InlineKeyboardButton(get_text("processed", context), callback_data=f"process_{i}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("Дії:", reply_markup=reply_markup)
    keyboard = [
        [InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: Processed orders
async def processed_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    processed = [o for o in data["orders"] if o.get("processed", False)]
    if not processed:
        await query.message.reply_text(get_text("no_processed_orders", context))
    else:
        for order in processed:
            name = data["clients"].get(str(order.get("user_id")), {}).get("admin_name") or order.get("name", "unknown")
            text = get_text(
                "order_info", context,
                name=name,
                phone=order.get("phone", "unknown"),
                description=order.get("description", "unknown"),
                address=order.get("address", "unknown"),
                date=order.get("date", "unknown"),
                time=order.get("time", "unknown"),
                status=get_text("processed", context)
            )
            await query.message.reply_text(text)
    keyboard = [
        [InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: Mark order as processed
async def process_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    index = int(query.data.split("_")[1])
    new_orders = [o for o in data["orders"] if not o.get("processed", False)]
    if 0 <= index < len(new_orders):
        for i, order in enumerate(data["orders"]):
            if order == new_orders[index]:
                data["orders"][i]["processed"] = True
                save_data(data)
                name = data["clients"].get(str(order.get("user_id")), {}).get("admin_name") or order.get("name", "unknown")
                await query.message.reply_text(
                    get_text("order_processed", context, name=name)
                )
                break
    keyboard = [
        [InlineKeyboardButton(get_text("back", context), callback_data="new_orders")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: Client list
async def client_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    if not data["clients"]:
        await query.message.reply_text(get_text("no_clients", context))
    else:
        for user_id, client_info in data["clients"].items():
            name = client_info.get("admin_name") or client_info.get("original_name", "unknown")
            keyboard = [[InlineKeyboardButton(get_text("client", context, name=name), callback_data=f"client_{user_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(get_text("client", context, name=name), reply_markup=reply_markup)
    keyboard = [
        [InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: View client orders
async def view_client_orders(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id=None) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    if not user_id:
        user_id = query.data.split("_")[1]
    client_orders = [o for o in data["orders"] if str(o.get("user_id")) == user_id]
    client_info = data["clients"].get(user_id, {})
    name = client_info.get("admin_name") or client_info.get("original_name", "unknown")
    for order in client_orders:
        status = get_text("processed", context) if order.get("processed", False) else get_text("not_processed", context)
        text = get_text(
            "order_info", context,
            name=name,
            phone=order.get("phone", "unknown"),
            description=order.get("description", "unknown"),
            address=order.get("address", "unknown"),
            date=order.get("date", "unknown"),
            time=order.get("time", "unknown"),
            status=status
        )
        await query.message.reply_text(text)
    keyboard = [
        [InlineKeyboardButton(get_text("edit_client_name", context), callback_data=f"edit_name_{user_id}")],
        [InlineKeyboardButton(get_text("back", context), callback_data="client_list")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: Edit client name
async def edit_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    user_id = query.data.split("_")[2]
    context.user_data["step"] = "edit_client_name"
    context.user_data["edit_client_id"] = user_id
    await query.message.reply_text(get_text("enter_new_client_name", context))

# Admin: List administrators
async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    await query.message.reply_text(get_text("list_admins_title", context))
    for admin_id, admin_info in data["admins"].items():
        name = admin_info["name"]
        keyboard = []
        if admin_id != str(ADMIN_ID):  # Main admin cannot be removed
            keyboard.append([InlineKeyboardButton(get_text("remove_admin", context), callback_data=f"remove_admin_{admin_id}")])
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        await query.message.reply_text(
            get_text("admin_info", context, name=name, id=admin_id),
            reply_markup=reply_markup
        )
    keyboard = [
        [InlineKeyboardButton(get_text("add_admin", context), callback_data="add_admin")],
        [InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Admin: Add administrator
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    context.user_data["step"] = "add_admin_id"
    await query.message.reply_text(get_text("enter_admin_id", context))

# Admin: Remove administrator
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    admin_id = query.data.split("_")[2]
    if admin_id == str(ADMIN_ID):
        await query.message.reply_text(get_text("cannot_remove_main_admin", context))
        return
    if admin_id in data["admins"]:
        name = data["admins"][admin_id]["name"]
        del data["admins"][admin_id]
        save_data(data)
        await query.message.reply_text(
            get_text("admin_removed", context, name=name, id=admin_id)
        )
    await list_admins(update, context)

# Admin: Remove booking
async def remove_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    keyboard = []
    for slot, name in data["bookings"].items():
        date, time = slot.split("_")
        keyboard.append([InlineKeyboardButton(f"🗓 {date} {time} ({name})", callback_data=f"remove_{slot}")])
    if not keyboard:
        await query.message.reply_text(get_text("no_bookings", context))
        keyboard = [
            [InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")],
            [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)
        return
    keyboard.append([InlineKeyboardButton(get_text("back", context), callback_data="admin_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("select_booking", context), reply_markup=reply_markup)

# Admin: Confirm remove booking
async def confirm_remove_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if str(query.from_user.id) not in data["admins"]:
        await query.message.reply_text(get_text("access_denied", context))
        return
    slot = query.data
    parts = slot.split("_")
    if len(parts) < 2 or parts[0] != "remove":
        await query.message.reply_text(get_text("error", context))
        return
    slot_key = "_".join(parts[1:])
    name = data["bookings"].get(slot_key, "unknown")
    if slot_key in data["bookings"]:
        del data["bookings"][slot_key]
        save_data(data)
        await query.message.reply_text(
            get_text("booking_removed", context, slot=slot_key, name=name)
        )
    else:
        await query.message.reply_text(
            get_text("booking_not_found", context, slot=slot_key)
        )
    keyboard = [
        [InlineKeyboardButton(get_text("back", context), callback_data="remove_booking")],
        [InlineKeyboardButton(get_text("main_menu", context), callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(get_text("return_to_main", context), reply_markup=reply_markup)

# Handle button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    try:
        data_type = query.data.split("_")[0]
    except IndexError:
        data_type = query.data

    if data_type == "create" and query.data in ["create_order", "create_another_order"]:
        await create_order(update, context)
    elif data_type == "personal":
        await personal_cabinet(update, context)
    elif data_type == "change" and query.data == "change_language":
        await change_language(update, context)
    elif data_type == "lang":
        await set_language(update, context)
    elif data_type == "date":
        await show_time_slots(update, context)
    elif data_type == "time":
        await confirm_order(update, context)
    elif data_type == "back" and query.data == "back_to_order":
        context.user_data["step"] = "address"
        await query.message.reply_text(get_text("enter_address", context))
    elif data_type == "back" and query.data == "back_to_date":
        await show_calendar(update, context)
    elif data_type == "prev":
        year, month = map(int, query.data.split("_")[2:])
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        context.user_data["calendar"] = {"year": year, "month": month}
        await show_calendar(update, context)
    elif data_type == "next":
        year, month = map(int, query.data.split("_")[2:])
        month += 1
        if month > 12:
            month = 1
            year += 1
        context.user_data["calendar"] = {"year": year, "month": month}
        await show_calendar(update, context)
    elif data_type == "main":
        user_id = str(update.effective_user.id)
        if user_id in data["admins"]:
            await admin(update, context)
        else:
            keyboard = [
                [InlineKeyboardButton(get_text("create_order", context), callback_data="create_order")],
                [InlineKeyboardButton(get_text("personal_cabinet", context), callback_data="personal_cabinet")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(get_text("welcome", context), reply_markup=reply_markup)
    elif data_type == "admin" and query.data == "admin_menu":
        await admin(update, context)
    elif data_type == "new":
        await new_orders(update, context)
    elif data_type == "processed":
        await processed_orders(update, context)
    elif data_type == "process":
        await process_order(update, context)
    elif data_type == "client" and query.data == "client_list":
        await client_list(update, context)
    elif data_type == "client":
        await view_client_orders(update, context)
    elif data_type == "edit" and query.data.startswith("edit_name"):
        await edit_client_name(update, context)
    elif data_type == "list" and query.data == "list_admins":
        await list_admins(update, context)
    elif data_type == "add" and query.data == "add_admin":
        await add_admin(update, context)
    elif data_type == "remove" and query.data.startswith("remove_admin"):
        await remove_admin(update, context)
    elif data_type == "remove" and query.data.startswith("remove_booking"):
        await remove_booking(update, context)
    elif data_type == "remove":
        await confirm_remove_booking(update, context)
    else:
        await query.message.reply_text(get_text("error", context))

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("Admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order_input))
    app.add_handler(MessageHandler(filters.CONTACT, handle_order_input))
    app.add_handler(MessageHandler(filters.PHOTO, handle_order_input))
    
    print("🚀 Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()