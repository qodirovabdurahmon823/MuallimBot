from filters.private_chat_filter import IsPrivate

from aiogram import types

from data.config import ADMINS
from keyboards.default.buttons import main, back_main, back_lessons_books
from loader import dp, db, bot, booksdb, lessonsdb
from aiogram.dispatcher import FSMContext
from handlers.users.actions import books_action, lessons_action


@dp.callback_query_handler(IsPrivate(), text_contains="get_book")
async def get_book(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    subject = callback.data.split(":")[1]
    book = callback.data.split(":")[2]
    file_id = booksdb.get_book(book, subject)[0]
    message_id = booksdb.get_book(book, subject)[1]

    await callback.message.delete()
    try:
        await callback.message.answer_document(file_id, caption=f"📕 <b>{subject}</b>dan <b>{book}</b>, kitobi tayyor yuqorida yuklab olishingiz mumkin !", reply_markup=back_lessons_books(subject, "books"))
    except:
        await bot.copy_message(message_id=message_id, chat_id=callback.from_user.id, from_chat_id="-1002256408723", caption=f"📕 <b>{subject}</b>dan <b>{book}</b>, kitobi tayyor yuqorida yuklab olishingiz mumkin !", reply_markup=back_lessons_books(subject, "books"))


@dp.callback_query_handler(IsPrivate(), text_contains="get_lesson")
async def get_lesson(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    subject = callback.data.split(":")[1]
    lesson = callback.data.split(":")[2]
    file_id = lessonsdb.get_lesson(lesson, subject)[0]
    message_id = lessonsdb.get_lesson(lesson, subject)[1]

    await callback.message.delete()
    try:
        await callback.message.answer_document(file_id, caption=f"📕 <b>{subject}</b>dan <b>{lesson}</b>, darsi tayyor yuqorida yuklab olishingiz mumkin !", reply_markup=back_lessons_books(subject, "lessons"))
    except:
        await bot.copy_message(message_id=message_id, chat_id=callback.from_user.id, from_chat_id="-1002256408723", caption=f"📕 <b>{subject}</b>dan <b>{lesson}</b>, darsi tayyor yuqorida yuklab olishingiz mumkin !", reply_markup=back_lessons_books(subject, "lessons"))

@dp.callback_query_handler(IsPrivate(), text_contains="back_book_lessons")
async def back_book_lessons(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    await callback.message.delete()

    action = callback.data.split(":")[1]
    subject = callback.data.split(":")[2]
    if action == "books":
        await books_action(callback.message, subject, action_type="send")
    elif action == "lessons":
        await lessons_action(callback.message, subject, action_type="send")

