from flask import Flask
from flask_restful import Resource, Api, reqparse
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext, Updater
from telegram import Update
import hashlib
import pymongo
from crontab import CronTab


class Schedule(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userHash', required=True)
        parser.add_argument('taskName', required=True)
        parser.add_argument('taskID', required=True)
        parser.add_argument('task', required=True)
        parser.add_argument('time', required=True)

        args = parser.parse_args()
        cron = CronTab(user='pratham')
        job = cron.new(
            command=f"python3 messenger.py {args['userHash']} {args['task']}", comment=args['taskID'])


class Done(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userHash', required=True)
        parser.add_argument('taskID', required=True)

        args = parser.parse_args()
        cron = CronTab(user='pratham')
        for job in cron:
            if job.comment == args['taskID']:
                cron.remove(job)
                cron.write()


app = Flask(__name__)
api = Api(app)
api.add_resource(Schedule, '/schedule')


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
userHashDb = myclient["UserHashDatabase"]

userCollection = userHashDb['users']


updater = Updater(
    token="5072089176:AAFOIvxmS-54Ph_01LY33jtf5EdPu15TxPE", use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    current_id = update.effective_chat.id
    hashval = hashlib.sha256(str(current_id).encode()).hexdigest()
    if userCollection.count_documents(filter={"hash": hashval}) == 0:
        userCollection.insert_one({"hash": hashval, 'userid': str(current_id)})
    message = "Hey welcome to Symphony!!\nPaste this code in vscode to register\n\n" + hashval
    context.bot.send_message(
        chat_id=current_id, text=message)


start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)
updater.start_polling()

if __name__ == '__main__':
    app.run()
