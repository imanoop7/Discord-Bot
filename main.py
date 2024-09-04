import discord
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()



intents = discord.Intents.default()
client = discord.Client(intents=intents)

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
    """Called when a message is sent in any channel the bot can see.
    
    If the message is sent by the bot itself, this function does nothing.
    Otherwise, if the message starts with '$hello', this function sends a
    message to the same channel with the content 'Hello!'.
    """
    
    if message.author == client.user:
        return

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)



client.run(os.getenv('TOKEN'))

