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

@client.event
async def on_ready():
    """Prints a message when the bot is ready."""
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author != client.user:
        if client.user in message.mentions:
            await message.channel.send(f'Hi {message.author.mention}, I am your bot.')

client.run(os.getenv('TOKEN'))