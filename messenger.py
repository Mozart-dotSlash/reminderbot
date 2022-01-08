import telegram
import sys
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
userHashDb = myclient["UserHashDatabase"]
userCollection = userHashDb['users']

bot = telegram.Bot(token="5072089176:AAFOIvxmS-54Ph_01LY33jtf5EdPu15TxPE")

bot.send_message(task=sys.argv[2], chat_id=userCollection.find(
    sys.argv[1]).next()['userid'])
