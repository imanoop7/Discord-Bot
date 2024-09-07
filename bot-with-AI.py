import discord
import os
import requests
import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama


# Load environment variables from the .env file
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Create the client with the updated intents
client = discord.Client(intents=intents)


def model_response(question: str) -> str:
    """
    Sends a question to the Ollama model and returns the response.
    Args:
        question (str): The question from the user.

    Returns:
        str: The response from the Ollama model.
    """
    # The prompt is a template that is used to generate the input to the
    # Ollama model. The {question} part is replaced with the actual question
    # from the user.
    prompt = """You are a discord bot, you will help a user by answering questions{question}"""
    # The Ollama model is created with the specified parameters.
    llm = ChatOllama(
        model = "phi3",
        temperature = 0.8,
        num_predict = 256,
    )
    # The prompt is sent to the Ollama model to generate a response.
    ans = llm.invoke(prompt)
    # The response is printed to the console for debugging purposes.
    print(ans.content)
    # The response is then returned to the user.
    return ans.content


@client.event
async def on_ready():
    """Prints a message when the bot is ready."""
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author != client.user:
        if client.user in message.mentions:
            await message.channel.send(model_response(message.content))

client.run(os.getenv('TOKEN'))