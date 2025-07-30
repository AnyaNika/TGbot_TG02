import os
import asyncio
from aiogram import Bot, Dispatcher, F
from googletrans import Translator
from gtts import gTTS

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Создаем папку img, если её нет
if not os.path.exists('img'):
    os.makedirs('img')

@dp.message(F.photo)
async def save_photo(message: Message):
    # Скачиваем фото
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.reply("Фото сохранено!")

@dp.message(Command('voice'))
async def voice(message: Message):
    # Готовим текст и озвучиваем
    text = "Это голосовое сообщение, отправленное ботом."
    tts = gTTS(text, lang='ru')
    tts.save("voice.ogg")
    audio = FSInputFile("voice.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    # Очистка файлов
    os.remove("voice.ogg")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Бот умеет выполнять команды:\n/start\n/help\n/voice\nСохранение фото: все фото от пользователя сохраняются в папке `img`.\nГолосовое сообщение: отправьте команду `/voice` — бот отправит голосовое сообщение.\nПеревод текста: любое текстовое сообщение бот переведёт на английский и отправит ответом.")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я учебный бот, я могу сохранять фото, отправить текстовое сообщение и перевести текст на английский язык!")

@dp.message()
async def translate_text(message: Message):
    # Переводим текст на английский
    translated = await translator.translate(message.text, dest='en')
    # print(translated)
    # print(type(translated))
    await message.reply(f"Перевод на английский:\n{translated.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот запущен!")
    asyncio.run(main())