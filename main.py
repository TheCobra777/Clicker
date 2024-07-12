import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, FSInputFile
from config import BOT_TOKEN, IMAGE_PATH

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_token_values = {}

class botwebapp:

    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self._register_handlers()

    def _register_handlers(self):
        self.dp.message.register(self.cmd_start, Command(commands=["start"]))
        self.dp.message.register(self.handle_webapp_data)

    async def cmd_start(self, message: types.Message):
        """Обработчик начальной команды"""
        name = message.from_user.first_name
        user_id = message.from_user.id

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Кликер", web_app=WebAppInfo(url="https://thecobra777.github.io/test/"))]
        ])

        token_value = user_token_values.get(user_id, 0)
        text = (
            f"✨ Привет {name}\n\n"
            f"💰 Ты накликал {token_value}\n"
        )

        photo = FSInputFile(IMAGE_PATH)
        await self.bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )

    async def handle_webapp_data(self, message: types.Message):
        """Обрабатывает ответы от вебапп"""
        if message.web_app_data:
            data = message.web_app_data.data
            try:
                token_value = int(data)
                user_id = message.from_user.id
                user_token_values[user_id] = token_value
                
                name = message.from_user.first_name
                text = (
                    f"✨ Привет {name}\n\n"
                    f"💰 Ты накликал {token_value}\n"
                )
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Кликер", web_app=WebAppInfo(url="https://thecobra777.github.io/test/"))]
                ])
                
                photo = FSInputFile(IMAGE_PATH)
                await self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard
                )
            except ValueError:
                await message.answer("Получены некорректные данные")
        else:
            logging.warning(f"Получено сообщение без web_app_data: {message}")

async def main():
    bot_handler = botwebapp(bot, dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())