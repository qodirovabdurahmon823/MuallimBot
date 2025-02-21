from filters.private_chat_filter import IsPrivate

from aiogram import types

from keyboards.default.buttons import tests_type_button, books_button, lessons_button
from loader import dp, booksdb, lessonsdb
from aiogram.dispatcher import FSMContext

# Handle actions
@dp.callback_query_handler(IsPrivate(), state="*", text_contains="act")
async def handle_action(callback: types.CallbackQuery, state: FSMContext):
    
    await state.finish()
    
    action = callback.data.split(":")[1]
    subject = callback.data.split(":")[2]
    if action == "tests":
        await tests_action(callback.message, subject)
    elif action == "books":
        await books_action(callback.message, subject)
    elif action == "lessons":
        await lessons_action(callback.message, subject)


# Tests
async def tests_action(message, subject):
    await message.edit_text("📋 Bo'limlardan birini tanlang", reply_markup=tests_type_button(subject))

# Books
async def books_action(message: types.Message, subject: str, action_type = "edit"):
    if action_type == "edit":
        await message.edit_text(f"📕 <b>{subject}</b>, kitobni tanlang:", reply_markup=books_button(subject, booksdb.get_books(subject)))
    elif action_type == "send":
        await message.answer(f"📕 <b>{subject}</b>, kitobni tanlang:", reply_markup=books_button(subject, booksdb.get_books(subject)))

# Lessons
async def lessons_action(message: types.Message, subject: str, action_type = "edit"):
    if action_type == "edit":
        await message.edit_text(f"📕 <b>{subject}</b>, kitobni tanlang:", reply_markup=lessons_button(subject, lessonsdb.get_lessons(subject)))
    elif action_type == "send":
        await message.answer(f"📕 <b>{subject}</b>, kitobni tanlang:", reply_markup=lessons_button(subject, lessonsdb.get_lessons(subject)))


