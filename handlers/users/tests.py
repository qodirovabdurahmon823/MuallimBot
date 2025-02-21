from filters.private_chat_filter import IsPrivate
import sqlite3

from aiogram import types
import asyncio
from data.config import ADMINS
from keyboards.default.buttons import main, tests_type_button, get_tests_button, show_tests_pages, test_details_keyboard, rework_on_test
from loader import dp, db, bot, subjectsdb, testsdb
from aiogram.dispatcher import FSMContext

@dp.callback_query_handler(IsPrivate(), state="*", text_contains="type_test")
async def tests_type(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    
    action = callback.data.split(":")[1]
    subject = callback.data.split(":")[2]

    await callback.message.edit_text(text="📚 Testni tanlang!", reply_markup=get_tests_button(subject, testsdb.get_tests(subject=subject, limit=5, page=1, test_type=action), test_type=action))

async def attestation_tests(message, subject):
    await message.edit_text("📋 Bo'limlardan birini tanlang", reply_markup=tests_type_button(subject))

async def themed_tests(message, subject):
    await message.edit_text("📋 Bo'limlardan birini tanlang", reply_markup=tests_type_button(subject))


@dp.callback_query_handler(IsPrivate(), text_contains="paginate_tests", state="*")
async def admin_paginate_tests(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    subject = callback.data.split(":")[1]
    page = callback.data.split(":")[2]
    tests_type = callback.data.split(":")[3]
    if page == 'no_page':
        await callback.answer("❌ Bu sahifaga o'tib bo'lmaydi! Limitga yetildi!")
    else:
        await callback.message.edit_text("📚 Testlar ro'yxatidan kerakli testni tanlang yoki yangi test yarating!", reply_markup=get_tests_button(subject, testsdb.get_tests(subject=subject, limit=5, page=page, test_type=tests_type), test_type=tests_type))

@dp.callback_query_handler(IsPrivate(), text_contains="pages", state="*")
async def admin_pages(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    subject = callback.data.split(":")[1]
    type = callback.data.split(":")[2]
    await callback.message.edit_text("Sahifani tanlang!", reply_markup=show_tests_pages(subject, testsdb.get_tests(subject=subject, test_type=type), type))


@dp.callback_query_handler(IsPrivate(), text_contains="get_test", state="*")
async def user_get_test(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    test = callback.data.split(":")[1]
    test_details = testsdb.get_information(test)
    await callback.message.edit_text(f"<b>📕 Fan: </b>{test_details['subject']}\n\n"
                                     f"<b>✍️ Test nomi:</b> {test_details['test_name']}\n"
                                     f"<b>📍 Test savollar soni:</b> {test_details['total_questions']}\n"
                                     f"<b>⏰ Test savollari orasidagi vaqt:</b> {test_details['timer']}\n\n"
                                     f"<b>↪️ Testni do'stlar bilan ulashish uchun link:</b> https://t.me/PedagogUzbot?start=test{test}", reply_markup=test_details_keyboard(test))
    data = testsdb.get_test(test)
async def send_poll_question(user_id: int, state: FSMContext, test_details: dict):
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    questions = data['questions']
    
    if current_index >= data['total']:
        result_text = (
            f"<b>Test yakunlandi!</b>\n\n"
            f"<b>📕 Fan:</b> {data['subject']}\n"
            f"<b>✅ To'g'ri javoblar:</b> {data['correct']}\n"
            f"<b>❌ Noto'g'ri javoblar:</b> {data['wrong']}"
        )
        await bot.send_message(chat_id=user_id, text=result_text, parse_mode="HTML", reply_markup=rework_on_test(test=test_details['id']))
        await state.finish()
        return

    question = questions[current_index]
    poll_msg = await bot.send_poll(
        chat_id=user_id,
        question=question['question'],
        options=question['options'],
        type="quiz",
        correct_option_id=question['correct_option'],
        is_anonymous=False,
        open_period=test_details['timer']
    )
    await state.update_data(poll_id=poll_msg.poll.id, answered=False)
    asyncio.create_task(poll_timeout_handler(user_id, poll_msg.poll.id, test_details['timer']))

async def poll_timeout_handler(user_id: int, poll_id: str, open_period: int):
    await asyncio.sleep(open_period + 1)
    state = dp.current_state(user=user_id)
    data = await state.get_data()
    if data.get('poll_id') == poll_id and not data.get('answered', False):
        current_index = data.get('current_index', 0)
        wrong = data.get('wrong', 0) + 1
        await state.update_data(wrong=wrong, answered=True)
        await state.update_data(current_index=current_index + 1)
        test = data['test']
        test_details = testsdb.get_information(test)
        await send_poll_question(user_id, state, test_details)

@dp.callback_query_handler(text_contains="start_test", state="*")
async def start_test(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    test = callback.data.split(":")[1]
    test_details = testsdb.get_information(test)
    questions = testsdb.get_test(test)


    await state.update_data(
        test=test,
        questions=questions,
        current_index=0,
        correct=0,
        wrong=0,
        total=len(questions),
        subject=test_details['subject']
    )

    await send_poll_question(callback.from_user.id, state, test_details)
    await callback.answer()

@dp.poll_answer_handler()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    state = dp.current_state(user=poll_answer.user.id)
    data = await state.get_data()

    if data.get('poll_id') != poll_answer.poll_id:
        return
    await state.update_data(answered=True)
    
    current_index = data.get('current_index', 0)
    questions = data['questions']
    current_question = questions[current_index]
    chosen_option = poll_answer.option_ids[0] if poll_answer.option_ids else None

    if chosen_option == current_question['correct_option']:
        correct = data.get('correct', 0) + 1
        await state.update_data(correct=correct)
    else:
        wrong = data.get('wrong', 0) + 1
        await state.update_data(wrong=wrong)

    await state.update_data(current_index=current_index + 1)
    test = data['test']
    test_details = testsdb.get_information(test)
    await send_poll_question(poll_answer.user.id, state, test_details)