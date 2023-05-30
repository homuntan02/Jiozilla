from telebot.async_telebot import AsyncTeleBot
from jiozillaBot.credentials import bot_token, bot_user_name
import DatabaseUtils;
import hashlib

global bot
global TOKEN
TOKEN = bot_token

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['help'])
async def send_welcome(msg):
  await bot.reply_to(msg, "Welcome to Jiozilla!! \n" + "Use /start to login/initiate an accout")

@bot.message_handler(commands='start')
async def start(msg):
  currUserId = bot._user.id
  if not DatabaseUtils.user_in_users(currUserId) :
     DatabaseUtils.add_user(currUserId)

  await bot.reply_to(msg,"Your Credentials have bee successfully loaded\n" + 
                     "userId: " + str(currUserId) + "\n"
                     "Use /addOrg to add an organisation")

@bot.message_handler(commands = ['addOrg'])
async def addOrg(msg):
  orgName = msg.text.split(" ")[1]
  orgId = int(hashlib.sha1(orgName.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

  if not DatabaseUtils.org_id_in_organisations(orgId):
    DatabaseUtils.add_org(orgName)   

  #Reply
  await bot.reply_to(msg,"Success!! Your Organisation id is:" + str(orgId) + '\n' +
                    "Get your colleagues to use the /join " + str(orgId) + " to join your organisation")

@bot.message_handler(commands =['join'])
async def joinOrg(msg):
    orgName = msg.text.split(" ")[1]
    orgId = int(hashlib.sha1(orgName.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    if not DatabaseUtils.org_id_in_organisations(orgId):
      await bot.reply_to(msg, "Couldn't find organisation")
    else: 
      currUserId = bot._user.id
      orgName = DatabaseUtils.add_user_from_org(currUserId, orgId)
      #Reply
      await bot.reply_to(msg,"Success!! You are now a part of" + orgName + '\n' +
                    "Get your other colleagues to use the /join " + orgName + " to join your organisation")
# @bot.message_handler(commands = "showOrgs")
# async def showOrgs(msg):
#   DatabaseUtils.list_all_org_to_user()

@bot.message_handler(func=lambda message: True)
async def echo_msg(msg):
  await bot.reply_to(msg, msg.text)

import asyncio

asyncio.run(bot.polling())