import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, FSInputFile
from config import BOT_TOKEN, IMAGE_PATH

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_clicks = {}

class botwebapp:

    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self._register_handlers()

    def _register_handlers(self):
        self.dp.message.register(self.cmd_start, Command(commands=["start"]))
        self.dp.message.register(self.handle_webapp_data)

    async def cmd_start(self, message: types.Message):
        name = message.from_user.first_name
        user_id = message.from_user.id
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Кликер", web_app=WebAppInfo(url="https://thecobra777.github.io/Clicker/"))]
        ])
    
        token_value = user_clicks.get(user_id, 0)
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
        if message.web_app_
            data = json.loads(message.web_app_data.data)
            user_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name

            if data['action'] == 'click':
                token_value = data['count']
                user_clicks[user_id] = token_value
                
                name = message.from_user.first_name
                text = (
                    f"✨ Привет {name}\n\n"
                    f"💰 Ты накликал {token_value}\n"
                )
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Кликер", web_app=WebAppInfo(url="https://thecobra777.github.io/Clicker/"))]
                ])
                
                photo = FSInputFile(IMAGE_PATH)
                await self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard
                )
            elif data['action'] == 'getStats':
                sorted_users = sorted(user_clicks.items(), key=lambda x: x[1], reverse=True)
                stats = []
                for i, (user_id, clicks) in enumerate(sorted_users, 1):
                    user = await self.bot.get_chat(user_id)
                    username = user.username or user.first_name
                    stats.append(f"TOP {i} | @{username} - {clicks} Кликов")
                
                stats_text = "\n".join(stats)
                await message.answer(stats_text)
        else:
            logging.warning(f"Получено сообщение без web_app_ {message}")

async def main():
    bot_handler = botwebapp(bot, dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
