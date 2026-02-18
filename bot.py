import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загадки и ответы
QUEST = [
    {"answer": "ШАНТИ", "task": "Кто-то настолько любит кушать, что потерял добро под своей миской. Кто это был?"},
    {"answer": "ЗЕРКАЛО", "task": "Загадка 2: Я показываю тебя, но не я. Что это?"},
    {"answer": "КНИГА", "task": "Загадка 3: Я молчу, но рассказываю истории. Что это?"}
]

# Прогресс пользователей
user_progress = {}
letters = {}

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user_progress[user_id] = 0
    letters[user_id] = []
    await message.answer("Начинаем квест!\n\n" + QUEST[0]["task"])

@dp.message()
async def check_answer(message: Message):
    user_id = message.from_user.id

    if user_id not in user_progress:
        return

    step = user_progress[user_id]
    correct_answer = QUEST[step]["answer"]

    user_input = message.text.strip().upper()

    if user_input == correct_answer:
        letters[user_id].append(correct_answer[0])
        step += 1
        user_progress[user_id] = step

        if step < len(QUEST):
            await message.answer("Верно!\n\n" + QUEST[step]["task"])
        else:
            final_word = "".join(letters[user_id])
            await message.answer(
                f"Ты прошла все этапы!\n\n"
                f"Собери первые буквы слов.\n"
                f"Итоговое место: {final_word}"
            )
    else:
        await message.answer("Неверно. Попробуй ещё.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

from aiogram.filters import Command

@dp.message(Command("reset"))
async def reset_progress(message: Message):
    user_id = message.from_user.id

    if user_id in user_progress:
        del user_progress[user_id]
    if user_id in letters:
        del letters[user_id]

    await message.answer("Прогресс сброшен. Напиши /start чтобы начать заново.")
