import telegram
import sys
import pymongo
import os
from crontab import CronTab


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
userHashDb = myclient["UserHashDatabase"]
userCollection = userHashDb['users']

bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])

bot.send_message(task=sys.argv[2], chat_id=userCollection.find(
    sys.argv[1]).next()['userid'])

cron = CronTab(user=os.environ['USER'])

for job in cron:
    if job.comment == sys.argv[3]:
        cron.remove(job)
        cron.write()
