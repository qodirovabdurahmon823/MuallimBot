from filters.private_chat_filter import IsPrivate
import sqlite3

from aiogram import types

from data.config import ADMINS
from keyboards.default.buttons import main, test_details_keyboard
from loader import dp, db, testsdb
from .tests import user_get_test
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsPrivate(), commands=['start'])
async def start_bot(message: types.Message):
    args = message.get_args()

    try:
        test_id = args.replace('test', '')
        test_details = testsdb.get_information(test_id)
        
        await message.answer(f"<b>📕 Fan: </b>{test_details['subject']}\n\n"
                                        f"<b>✍️ Test nomi:</b> {test_details['test_name']}\n"
                                        f"<b>📍 Test savollar soni:</b> {test_details['total_questions']}\n"
                                        f"<b>⏰ Test savollari orasidagi vaqt:</b> {test_details['timer']}\n\n"
                                        f"<b>↪️ Testni do'stlar bilan ulashish uchun link:</b> https://t.me/PedagogUzbot?start=test{test_id}", reply_markup=test_details_keyboard(test_id))

        return
    except:
        pass
    
    await message.answer(f"<b>👋 Assalomu alaykum <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>, botimizga xush kelibsiz!</b>\n\n👇 Quyida o‘zingizga kerakli bo‘limni tanlang !", reply_markup=main)
    
    try:
        db.add_user(message.from_user.id, message.from_user.full_name, username=message.from_user.username)
    except Exception as e:
        pass



@dp.callback_query_handler(IsPrivate(), text_contains="check_subs")
async def check_subs(call: types.CallbackQuery, state: FSMContext):
    test_id = call.data.split(":")[1]
    if test_id == "None":
        await call.message.delete()
        try:db.add_user(call.from_user.id, call.from_user.full_name, username=call.from_user.username)
        except:pass
        await start_bot(call.message)
    else:
        await user_get_test(call, state)
        
        
    


