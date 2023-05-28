from telebot.async_telebot import AsyncTeleBot
from jiozillaBot.credentials import bot_token, bot_user_name

global bot
global TOKEN
TOKEN = bot_token

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(msg):
  await bot.reply_to(msg, "I am your mom" + bot_user_name)

@bot.message_handler(func=lambda message: True)
async def echo_msg(msg):
  await bot.reply_to(msg, msg.text)

import asyncio

asyncio.run(bot.polling())