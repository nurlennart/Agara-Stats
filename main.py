import pymongo
import asyncio
from configparser import ConfigParser
import sys
import curses
from curses import wrapper
import os

parser = ConfigParser()
parser.read('config.ini')

# init curses screen
stdscr = curses.initscr()
stdscr.keypad(1)

# stuff for delay
justStarted = True

if justStarted == True:
    delay = 5
    justStarted == False
else:
    delay = int(parser.get('refresh_delay', 'delay'))

# init database
mongo_client = pymongo.MongoClient("mongodb+srv://" + str(parser.get('mongodb', 'auth_string')) + "@cluster0-1fhvf.mongodb.net/agara?retryWrites=true")
db = mongo_client['agara']

# initialize
async def init():
    stdscr.addstr(0, 0, "started. time to pull some stats..")
    stdscr.refresh()

    while True:
        await runStats()

# function to run the stats function
async def runStats():
    await asyncio.sleep(delay)
    showCurrentStats()

# render the stats
def showCurrentStats():
    # vars to display
    user_count = getUserCount()
    message_count = getMessageCount()
    total_balance = getTotalBalance()

    # clear and refresh the screen
    stdscr.clear()
    stdscr.addstr(0, 0, "==== Agara Stats ====")
    stdscr.addstr(0, 50, "Updated every {0} seconds".format(int(parser.get('refresh_delay', 'delay'))))
    stdscr.addstr(1, 0, "Messagecount in Database: {0}".format(message_count))
    stdscr.addstr(2, 0, "Users in Database: {0}".format(user_count))
    stdscr.addstr(3, 0, "Total Balance from all users in db: {0}".format(total_balance))

    # refresh screen
    stdscr.refresh()

# count users in database and return count
def getUserCount():
    users = db.currencysystem

    user_count = users.estimated_document_count()

    return(user_count)

# count messages of all users in database and return count
def getMessageCount():
    messagecount = 0

    users = db.currencysystem
    cursor = users.find()

    for document in cursor:
        messagecount += int(document['messagecount'])

    return(messagecount)

# sum balance of all users in database and return balance
def getTotalBalance():
    balance = 0

    users = db.currencysystem
    cursor = users.find()

    for document in cursor:
        balance += int(document['balance'])

    return(balance)

# run.
asyncio.run(init())
