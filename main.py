import discord
import os
from dotenv import load_dotenv

load_dotenv()



intents = discord.Intents.default()
client = discord.Client(intents=intents)

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(os.getenv('TOKEN'))

