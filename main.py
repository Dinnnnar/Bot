import asyncio
import logging
import sys
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
import messages
import sqlite
from coordinates import Coordinates
import datetime
from sqlite import cloth
import aioschedule
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

TOKEN = "6228920120:AAFfSONwpoqYiH4r3kqaqU94FImGFpk8piU"

dp = Dispatcher(storage=MemoryStorage())
HELPCOMMAND = """
/help - помощь
/start - запуск бота
/weathercity - погода у города, который вы укажете
"""
PICTUREHELP = ["https://i.imgur.com/wgYIKr3.jpg",
               "https://yt3.ggpht.com/Z1aEpn6VOMBjHghE6CHVO4lkQchQBPVlQJXUq58ONkNoVIkQDW_9A936qmA5DNDc3oCUZVMNLg=s900-c-k-c0x00ffffff-no-rj",
               "https://wallpapercave.com/wp/wp10029622.jpg",
               "https://www.pngkit.com/png/detail/16-162183_anime-png.png", "https://i.imgur.com/L2WtcTx.jpg"]
WEATHERCOLD = ["https://i.pinimg.com/736x/f3/33/26/f33326a5126e7d4588e8f8b76c4fcd17.jpg",
               "https://kartinkin.net/pics/uploads/posts/2022-09/1662858128_15-kartinkin-net-p-zamerzshii-kot-vkontakte-15.jpg",
               "https://krasivosti.pro/uploads/posts/2021-04/thumbs/1617887634_49-p-kot-v-odeyale-59.jpg",
               "https://adonius.club/uploads/posts/2022-05/1653866720_19-adonius-club-p-kot-v-pukhovike-krasivo-foto-22.jpg"]
WEATHERHOT = [
    "https://api.rbsmi.ru/attachments/39e43c7c57092eff2db88a81307d8f051578cde7/store/crop/0/0/893/593/1600/0/0/a0d7c3a112f35d6c10031773f41828c888d580289a3adeb06d0b352da0f2/4d398c1a16b8d4f36a6abda51dd49e77.jpg",
    "https://krasivosti.pro/uploads/posts/2021-07/1625868785_54-krasivosti-pro-p-kotu-zharko-koti-krasivo-foto-58.jpg",
    "https://krasivosti.pro/uploads/posts/2021-07/1625868786_17-krasivosti-pro-p-kotu-zharko-koti-krasivo-foto-18.jpg"]
CITY = ["Москва", "Лениногорск", "Казань", "Самара"]


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text=f"/weathercity {random.choice(CITY)}")],
        [types.KeyboardButton(text="Узнать погоду", request_location=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True)
    await message.answer(text=f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard)
    await message.answer_sticker(sticker='CAACAgIAAxkBAAJUbWUpI7Uc0qHUQ-UyjTBBBzKGCrJuAAIVAAPANk8TzVamO2GeZOcwBA')
    while True:
        await asyncio.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == '23:44:01':
            await message.send_message(message.chat.id, f'"Это сообщение отправлено в {current_time}"')


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer_photo(photo=random.choice(PICTUREHELP), caption=HELPCOMMAND)


@dp.message(F.location)
async def loc_handler(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    loc = Coordinates(latitude=lat, longitude=lon)
    wthr = await messages.weather(loc)
    response_text = await sqlite.cloth(wthr.temperature)
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(loc_handler, trigger=CronTrigger(hour=18, minute=00),
                      kwargs={'message':message})
    scheduler.add_job(loc_handler, trigger=CronTrigger(hour=8, minute=00),
                      kwargs={'message':message})
    await message.answer_photo(photo=f"{random.choice(WEATHERCOLD)}",
                               caption=f'{wthr.location}, {wthr.description}\n' \
                                       f'Температура - {wthr.temperature}°C, ощущается, как {wthr.temperature_feeling}°C. {response_text}')


@dp.message(Command("weathercity"))
async def weather(message: types.Message, command: CommandObject):
    kb = [
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text=f"/weathercity {random.choice(CITY)}")],
        [types.KeyboardButton(text="Узнать погоду", request_location=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True)

    if command.args:
        wthr = await messages.weather_for_city(command.args)
        response_text = await sqlite.cloth(wthr.temperature)
        await message.answer_photo(photo=f"https://cataas.com/cat/says/{command.args}", caption=f'{command.args}, {wthr.description}\n' \
                                           f'Температура - {wthr.temperature}°C, ощущается, как {wthr.temperature_feeling}°C. {response_text}',
                                           reply_markup=keyboard)
    else:
        await message.answer("Пожалуйста напишете город после команды /weathercity")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
