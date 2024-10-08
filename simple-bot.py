import discord
import os
import requests
import json
from dotenv import load_dotenv
import random
import pymongo

load_dotenv()

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["mydatabase"]
collection = db["mycollection"]

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
client = discord.Client(intents=intents)

sad_words = ['sad', 'depressed', 'unhappy', 'angry', "miserable", "derpressing"]

starter_encouragements = ["Cheer up!", "Hang in there", "You are a great person / bot!"]

def get_quote():
    """Retrieves a random quote from the ZenQuotes API.
    
    This function sends a GET request to the ZenQuotes API and parses the
    response to extract a random quote and its author. The quote and author
    are concatenated and then returned.
    """
    
    print("Sending GET request to the ZenQuotes API")
    response = requests.get("https://zenquotes.io/api/random")
    print("Parsing response")
    json_data = json.loads(response.text)
    print("Extracting quote and author")
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    print(f"Returning quote: {quote}")
    return(quote)


def update_encouragements(encouraging_message):
    """Updates the list of encouragements in the database with a new message.

    If the list does not exist, this function creates it with the given message.
    Otherwise, it appends the message to the existing list.

    Args:
        encouraging_message (str): The message to add to the list of
            encouragements.
    """
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    """Deletes an encouragement from the database at a given index.

    Args:
        index (int): The index of the encouragement to delete.
    """
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

@client.event
async def on_ready():
    """Prints a message when the bot is ready.
    
    This function is called after the bot has successfully logged in.
    It prints a message to the console indicating that the bot is ready.
    The message includes the bot's username.
    """
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    """This function is called when a message is sent in any channel that the
    bot can see. It checks if the message author is the bot itself, and if
    so, it returns without doing anything.

    Otherwise, it checks if the message starts with various commands and
    performs different actions based on the command.

    The possible commands are:

    - $inspire: sends a random inspirational quote
    - $new <message>: adds a new encouragement to the list of encouragements
    - $del <index>: deletes an encouragement from the list of encouragements
    - $list: sends a list of all the encouragements
    - $responding <true/false>: turns responding on or off. If set to true,
        the bot will respond with an encouragement if it sees a sad word in
        the message. If set to false, the bot won't respond to anything."""
    
    if message.author == client.user:
        return
    
    msg = message.content.lower()

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements

    if "encouragements" in db.keys():
        options = options + db["encouragements"]
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New Encouragement added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del",1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")




client.run(os.getenv('TOKEN'))

