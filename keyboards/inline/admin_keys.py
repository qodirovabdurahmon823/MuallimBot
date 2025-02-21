from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.callback_data import CallbackData
from loader import bot


admin_panel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Reklama", callback_data='admin:announcement'),
            InlineKeyboardButton(text="🔐 Majburiy Obuna", callback_data='admin:subscription'),

        ],
        [
            InlineKeyboardButton(text="📚 Darsliklar", callback_data='admin:books'),
            InlineKeyboardButton(text="📒 Dars ishlanmalari", callback_data='admin:lessons'),
        ],
        [
            InlineKeyboardButton(text="📝 Testlar", callback_data='admin:tests'),
            InlineKeyboardButton(text="📊 Statistika", callback_data='admin:statistics'),
        ],
    ],
)

admin_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back'),
        ]
    ],
)

async def channels_list_builder(channels_list):
    keyboard = InlineKeyboardMarkup()
    for channel in channels_list:
        info = await bot.get_chat(channel)
        title = info.title
        keyboard.add(InlineKeyboardButton(text=title, callback_data=f"admin:channel:{channel}"))

    keyboard.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="admin:add_channel"))
    keyboard.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back'))
    return keyboard

def channel_details_keyboard(username):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🗑 Ro'yxatdan olib tashlash", callback_data=f"admin:delete_channel:{username}"))
    username = username.replace("@", "")
    keyboard.add(InlineKeyboardButton(text="🔗 Kanalga o'tish", url=f"https://t.me/{username}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back_channels_list'))
    return keyboard


back_channels_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back_channels_list')
        ]
    ]
)

def admin_subjects_button(action, subjects):
	buttons = InlineKeyboardMarkup(row_width=2)

	for subject in subjects:
		buttons.insert(InlineKeyboardButton(subject, callback_data=f"admin:action:{action}:{subject}"))
    
	buttons.add(InlineKeyboardButton("➕ Fan qo'shish", callback_data="admin:add_subject"))
	buttons.add(InlineKeyboardButton("🔙 Ortga", callback_data="admin:back"))
	return buttons


def admin_books_button(subject, books):
    keyboard = InlineKeyboardMarkup(row_width=2)
    books.sort()
    for book in books:
        keyboard.insert(InlineKeyboardButton(text=book[0], callback_data=f"admin:get_book:{subject}:{book[0]}"))

    keyboard.add(InlineKeyboardButton(text="🗑 Fanni o'chirish", callback_data=f'admin:delete_subject:{subject}'))
    keyboard.insert(InlineKeyboardButton(text="➕ Kitob qo'shish", callback_data=f"admin:add_book:{subject}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back_subjects:books'))
    return keyboard

def admin_lessons_button(subject, lessons):
    keyboard = InlineKeyboardMarkup(row_width=2)
    lessons.sort()

    for lesson in lessons:
        keyboard.insert(InlineKeyboardButton(text=lesson[0], callback_data=f"admin:get_lesson:{subject}:{lesson[0]}"))
    keyboard.add(InlineKeyboardButton(text="🗑 Fanni o'chirish", callback_data=f'admin:delete_subject:{subject}'))
    keyboard.insert(InlineKeyboardButton(text="➕ Dars ishlanmasi qo'shish", callback_data=f"admin:add_lesson:{subject}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data='admin:back_subjects:lessons'))
    return keyboard


def admin_back_lessons_books(subject, action, name):
    if action == "books":
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton("♻️ Kitobni alishtirish", callback_data=f"admin:edit_book:{subject}:{name}")
        ],
		[
			InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_book_lessons:{action}:{subject}")
		]
	])
    elif action == "lessons":
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton("♻️ Dars ishlanmasini alishtirish", callback_data=f"admin:edit_lesson:{subject}:{name}")
        ],
		[
			InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_book_lessons:{action}:{subject}")
		]
	])

def admin_back_lessons_books_2(subject, action):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_book_lessons:{action}:{subject}"))
    return keyboard



def admin_back_book_list(subject, action):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_book_lessons:{action}:{subject}"))
    return keyboard

advert_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("↪️ Forward", callback_data="admin:advert_type:forward"),
        InlineKeyboardButton("🔀 Oddiy", callback_data="admin:advert_type:simple"),
    ],
    [
         InlineKeyboardButton("🔙 Ortga", callback_data="admin:back")
    ]
])

def get_tests_button(subject, tests_details):

    if tests_details['has_next_page']:
        next_page = tests_details['next_page']
    else:
        next_page = 'no_page'
    
    if tests_details['has_previous_page']:
        previous_page = tests_details['previous_page']
    else:
        previous_page = 'no_page'
    
    if tests_details['last_page'] is tests_details['current_page'] or tests_details['last_page'] is None:
        last_page = "no_page"

    else:
        last_page = tests_details['last_page']

    if tests_details['first_page'] is tests_details['current_page'] or tests_details['first_page'] is None:
        first_page = "no_page"
    else:
        first_page = tests_details['first_page']
    if tests_details['total_pages'] == 0:
        total_pages = 1
    else:
        total_pages = tests_details['total_pages']

    keyboard = InlineKeyboardMarkup(row_width=5)
    for test in tests_details['tests']:
        keyboard.add(InlineKeyboardButton(test['name'], callback_data=f"admin:get_shmldrq:{subject}:{test['id']}"))
    keyboard.add(InlineKeyboardButton("⏮️", callback_data=f"admin:paginate_shmldrq:{subject}:{first_page}"))
    keyboard.insert(InlineKeyboardButton("⏪", callback_data=f"admin:paginate_shmldrq:{subject}:{previous_page}"))
    keyboard.insert(InlineKeyboardButton(f"{tests_details['current_page']}/{total_pages}", callback_data=f"admin:shmldrq:{subject}"))
    keyboard.insert(InlineKeyboardButton("⏩", callback_data=f"admin:paginate_shmldrq:{subject}:{next_page}"))
    keyboard.insert(InlineKeyboardButton("⏭️", callback_data=f"admin:paginate_shmldrq:{subject}:{last_page}"))
    keyboard.add(InlineKeyboardButton(text="🗑 Fanni o'chirish", callback_data=f'admin:delete_subject:{subject}'))
    keyboard.insert(InlineKeyboardButton("➕ Test yaratish", callback_data=f"admin:create_test:{subject}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_subjects:tests"))
    return keyboard

def show_tests_pages(subject, tests_details):
    keyboard = InlineKeyboardMarkup(row_width=8)
    total_pages = tests_details['total_pages']
    for page in range(1, total_pages+1):
        keyboard.insert(InlineKeyboardButton(f"{page}", callback_data=f"admin:paginate_shmldrq:{subject}:{page}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_tests_page:{subject}"))
    return keyboard




def get_test_button(subject, test):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data="admin:back"))
    return keyboard

shuffling_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton("🔀 Hammasini aralashtirish"),
        KeyboardButton("🔀 Savolni aralashtirish"),
    ],
    [
        KeyboardButton("🔀 Javobni aralashtirish"),
        KeyboardButton("🔀 Umuman aralashtirmaslik"),
    ],
    [
        KeyboardButton("🔙 Ortga")
    ]
], resize_keyboard=True)

def test_details_keyboard(subject, test):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("➕ Savol qo'shish", callback_data=f"admin:add_question:{subject}:{test}"))
    keyboard.add(InlineKeyboardButton("🔀 Alishtirish turini o'zgartirish", callback_data=f"admin:change_shuffling_type:{subject}:{test}"))
    keyboard.insert(InlineKeyboardButton("⏰ Taymerni o'zgartirish", callback_data=f"admin:change_time:{subject}:{test}"))
    keyboard.add(InlineKeyboardButton("🗑 Testni o'chirish", callback_data=f"admin:delete_test:{subject}:{test}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"admin:back_tests_page:{subject}"))
    return keyboard 