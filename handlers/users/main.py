from filters.private_chat_filter import IsPrivate

from aiogram import types

from data.config import ADMINS
from keyboards.default.buttons import main, back_main, subjects_button
from loader import dp, db, bot, subjectsdb
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


# Back buttons section
@dp.callback_query_handler(IsPrivate(), state="*", text="back")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await callback.message.edit_text(f"<b>👋 Assalomu alaykum <a href='tg://user?id={callback.from_user.id}'>{callback.from_user.full_name}</a>, botimizga xush kelibsiz!</b>\n\n👇 Quyida o‘zingizga kerakli bo‘limni tanlang !", reply_markup=main)


@dp.callback_query_handler(IsPrivate(), state="*", text="back_main")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()

    await callback.message.edit_text(f"<b>👋 Assalomu alaykum <a href='tg://user?id={callback.from_user.id}'>{callback.from_user.full_name}</a>, botimizga xush kelibsiz!</b>\n\n👇 Quyida o‘zingizga kerakli bo‘limni tanlang !", reply_markup=main)

@dp.message_handler(IsPrivate(), state="*", text="🔙 Ortga")
async def back_to_main_message(message: types.Message, state: FSMContext):

    await state.finish()
    await message.answer("🔙 Ortga", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"<b>👋 Assalomu alaykum <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>, botimizga xush kelibsiz!</b>\n\n👇 Quyida o‘zingizga kerakli bo‘limni tanlang !", reply_markup=main)



@dp.callback_query_handler(IsPrivate(), state="*", text_contains="back_subjects")
async def back_to_subjects(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    action = callback.data.split(":")[1]
    await callback.message.edit_text("📚 Fanni tanlang !", reply_markup=subjects_button(action=action, subjects=subjectsdb.get_subjects()))



# Tests section
@dp.callback_query_handler(IsPrivate(), state="*", text="tests")
async def tests(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await callback.message.edit_text("📚 Fanni tanlang !", reply_markup=subjects_button(action="tests", subjects=subjectsdb.get_subjects()))



# Books section
@dp.callback_query_handler(IsPrivate(), state="*", text="books")
async def books(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await callback.message.edit_text("📚 Fanni tanlang !", reply_markup=subjects_button(action="books", subjects=subjectsdb.get_subjects()))




# Lessons section
@dp.callback_query_handler(IsPrivate(), state="*", text="lessons")
async def lessons(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await callback.message.edit_text("📚 Fanni tanlang !", reply_markup=subjects_button(action="lessons", subjects=subjectsdb.get_subjects()))


# Ordering a feature
@dp.callback_query_handler(IsPrivate(), state="*", text="order")
async def order(callback: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await callback.message.edit_text("<b>📦 Buyutma berish\n\nSizga nima zarur ekanlgini batafsil yozib yuboring! Buni adminlar ko'rib chiqadi</b>", reply_markup=back_main)
    await state.set_state("order")

@dp.message_handler(IsPrivate(), state="order")
async def order_message(message: types.Message, state: FSMContext):
    await message.answer("👤 Adminga buyurtma jo'natildi. Yordamingiz uchun minnatdormiz!", reply_markup=back_main)
    for admin in ADMINS:
        await bot.send_message(admin, f"👤 <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> bot uchun buyurtma jo'natdi: \n<blockquote>{message.text}</blockquote>\n")
    await state.finish()

@dp.callback_query_handler(IsPrivate(), text='ommalashtirish')
async def ommalashtirish(call: types.CallbackQuery, state: FSMContext):
    key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
            types.InlineKeyboardButton("📷 Video qo'llanma", callback_data='video_guide'),
            types.InlineKeyboardButton("📝 Na'munalar", callback_data='lessons')
            ],
            [
            types.InlineKeyboardButton("🔙 Ortga", callback_data='back_main'),

            ]
        ]
    )
    await call.message.edit_text("Davom etish uchun ushbu bo'limlardan birni tanlang!", reply_markup=key)
