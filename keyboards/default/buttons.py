from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = InlineKeyboardMarkup(inline_keyboard=[
	[
		InlineKeyboardButton("❗️ TESTLAR (Attestatsiya)", callback_data="tests"),
		InlineKeyboardButton("📚 Darsliklar", callback_data="books")
        
	],
	[
		InlineKeyboardButton('🎓 Ommalashtirish.uz', callback_data='ommalashtirish'),
        InlineKeyboardButton("📦 Buyutma berish", callback_data="order")
        
	],
	[
	],
    [
        InlineKeyboardButton("🤖 Botni yaqinlarga ulashish", switch_inline_query="""Barcha fan o‘qituvchilari uchun!

Ushbu bot orqali quyidagilarni topishingiz mumkin:

⚡️ Barcha fanlardan attestatsiya testlari

⚡️ Barcha fanlardan mavzulashtirilgan testlar

⚡️ Amaldagi maktab darsliklari

⚡️ Ommalashtirish.uz platformasi uchun foydali manbaalar

Botga kiring va START tugmasini bosib o‘zingizga kerakli bo‘limni tanlang

@PedagogUzbot
@PedagogUzbot
@PedagogUzbot""")
	]


])

back_main = InlineKeyboardMarkup(inline_keyboard=[
	[
		InlineKeyboardButton("🔙 Ortga", callback_data="back_main")
	]
])
def subjects_button(action, subjects):
	buttons = InlineKeyboardMarkup(row_width=2)

	for subject in subjects:
		buttons.insert(InlineKeyboardButton(subject, callback_data=f"act:{action}:{subject}"))
	buttons.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
	return buttons


def tests_type_button(subject):
	buttons = InlineKeyboardMarkup(inline_keyboard=[
		[
			InlineKeyboardButton("Attestatsiya testlari", callback_data=f"type_test:attestation:{subject}"),
		],
		[
			InlineKeyboardButton("Mavzulashtirilgan testlar", callback_data=f"type_test:themed:{subject}"),
		],
		[
			InlineKeyboardButton("🔙 Ortga", callback_data="back_subjects:tests")
		]
	])

	return buttons

def back_lessons_books(subject, action):
	return InlineKeyboardMarkup(inline_keyboard=[
		[
			InlineKeyboardButton("🔙 Ortga", callback_data=f"back_book_lessons:{action}:{subject}")
		]
	])

def books_button(subject, books):
	buttons = InlineKeyboardMarkup(row_width=2)
	books = [book[0] for book in books]
	books.sort()

	for book in books:
		buttons.insert(InlineKeyboardButton(book, callback_data=f"get_book:{subject}:{book}"))

	buttons.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_subjects:books"))

	return buttons

def lessons_button(subject, lessons):
	buttons = InlineKeyboardMarkup(row_width=2)
	lessons = [lesson[0] for lesson in lessons]
	lessons.sort()

	for lesson in lessons:
		buttons.insert(InlineKeyboardButton(lesson, callback_data=f"get_lesson:{subject}:{lesson}"))
	
	buttons.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_subjects:lessons"))
	return buttons


	
def get_tests_button(subject, tests_details, test_type):

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
        keyboard.add(InlineKeyboardButton(test['name'], callback_data=f"get_test:{test['id']}"))
    keyboard.add(InlineKeyboardButton("⏮️", callback_data=f"paginate_tests:{subject}:{first_page}:{test_type}"))
    keyboard.insert(InlineKeyboardButton("⏪", callback_data=f"paginate_tests:{subject}:{previous_page}:{test_type}"))
    keyboard.insert(InlineKeyboardButton(f"{tests_details['current_page']}/{total_pages}", callback_data=f"pages:{subject}:{test_type}"))
    keyboard.insert(InlineKeyboardButton("⏩", callback_data=f"paginate_tests:{subject}:{next_page}:{test_type}"))
    keyboard.insert(InlineKeyboardButton("⏭️", callback_data=f"paginate_tests:{subject}:{last_page}:{test_type}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"back"))
    return keyboard

def show_tests_pages(subject, tests_details, test_type):
    keyboard = InlineKeyboardMarkup(row_width=8)
    total_pages = tests_details['total_pages']
    for page in range(1, total_pages+1):
        keyboard.insert(InlineKeyboardButton(f"{page}", callback_data=f"paginate_tests:{subject}:{page}:{test_type}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"back"))
    return keyboard

def test_details_keyboard(test):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("▶️ Boshlash", callback_data=f"start_test:{test}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"back"))
    return keyboard 
def rework_on_test(test):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton("▶️ Qayta ishlash", callback_data=f"start_test:{test}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data=f"back"))
    return keyboard 

