import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загадки и ответы
QUEST = [
    {"answer": "КУХНЯ", "task": "Добро пожаловать на твой день рождения! Играем в прятки! Ответ это одно слово. Когда догадаешься какое, просто впиши его сюда! Постарайся не сворачивать с маршрута и идти к точке только после того, как угадаешь слово, ведь этот квест неустойчив к ошибкам) Давай проверим как ты справишься с механикой! Где обитает друже Обломов? Там и ждет тебя первый подарок! Впиши название комнаты"},
    {"answer": "ДИВАН", "task": "Верно! Продолжай в том же духе. Следующая загадка ждет тебя на столе, вперед к подаркам!"},
    {"answer": "КССОЗЗКСО", "task": "Видишь кубик? Это твой куб удачи, давай проверим счастливчик ли ты. Вводи последовательно первые буквы названия цветов слева направо, сначала верхний ряд, потом средний и наконец нижний.  (верхний левый элемент помечен). Пример ответа ксжбккссз."},
    {"answer": "ШАНТИ", "task": "Справилась! Я надеюсь было не слишком сложно понять условия задачи). Следующий подарок там, куда стремятся все котики этого дома. Или под этим местом. А как зовут котика-владельца?"},
    {"answer": "ТОЛСТОЙ", "task": "Это от Ольги Юрьевны. Ищи подсказки в кроксе! Ну и шкаф купе можешь открыть заодно"},
    {"answer": "ПОДЪЕЗД", "task": "Так ты хочешь меня найти? Ходит-бродит тут. Страница 809, книга 1. Как сейчас звучит выделенное слово по-современному? Ищи меня там)"}
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
    
@dp.message(Command("reset"))
async def reset_progress(message: Message):
    user_id = message.from_user.id

    if user_id in user_progress:
        del user_progress[user_id]
    if user_id in letters:
        del letters[user_id]

    await message.answer("Прогресс сброшен. Напиши /start чтобы начать заново.")

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
            )
    else:
        await message.answer("Неверно. Попробуй ещё.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







