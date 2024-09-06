import discord
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Create the client with the updated intents
client = discord.Client(intents=intents)

def get_quote():
    """Retrieves a random quote from the ZenQuotes API."""
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@client.event
async def on_ready():
    """Prints a message when the bot is ready."""
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"Received message: {message.content}")
    if message.author == client.user:
        return
    msg = message.content.lower()
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    elif msg.startswith('$help'):
        await message.channel.send("Available commands: $inspire, $help")
    else:
        await message.channel.send("Sorry, I didn't understand that command.")

# Run the bot using the token from the environment variables
client.run(os.getenv('TOKEN'))
