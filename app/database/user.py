from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from database.requests import set_user, del_task, set_task
import keyboards as kb

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Натисніть на виконану задачу щоб видалити  або напишіть в чат нову.',
                         reply_markup=await kb.tasks(message.from_user.id))
    


@user.callback_query(F.data.startswith('task_'))
async def delete_task(callback: CallbackQuery):
    await del_task(callback.data.split('_')[1])
    await callback.message.delete()
    await callback.message.answer('Натисніть на виконану задачу щоб видалити  або напишіть в чат нову.',
                         reply_markup=await kb.tasks(callback.from_user.id))
    await callback.answer('Задача виконана')

@user.message()
async def add_task(message: Message):
    if len(message.text) > 100:
        await message.answer('Задача дуже довга')
        return
    await set_task(message.from_user.id, message.text)
    await message.answer('Задача додана\nНатисніть на виконану задачу щоб видалити  або напишіть в чат нову.',
                         reply_markup=await kb.tasks(message.from_user.id))
