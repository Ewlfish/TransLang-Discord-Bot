import discord
from discord.ext import commands
from translate import Translator

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True  # Enable the privileged intent

bot = commands.Bot(command_prefix='!', intents=intents)  # Bot prefix


async def on_ready():
    print(f'Bot connected as {bot.user.name}')

# IMPORTANT !!! #This token is different based on the user
bot_token = ''


async def on_message(message):
    if message.content == "hello":
        await message.reply("Hello!")


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')  # confirmation bot is online


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent potential infinite loops
    if message.author.bot:
        return

    # Check if the message content needs to be translated (e.g., based on a trigger word or specific channel)
    if "~" in message.content.lower():
        x = message.content.split()
        source_language = x[2]
        target_language = x[1]

        # Extract the text to be translated from the message content
        mx = message.content.split(" / ")
        text_to_translate = mx[1]

        # Create a translator object
        translator = Translator(
            from_lang=source_language, to_lang=target_language)
        # Translate the text
        translation = translator.translate(text_to_translate)

        # Send the translated text as a response
        await message.channel.send(translation)

    elif "`" in message.content.lower():
        target_user = message.mentions[0] if message.mentions else None
        source_language = message.author.top_role.name
        target_language = target_user.top_role.name

        # Extract the text to be translated from the message content
        rx = message.content.split(" - ")
        text_to_translate = rx[1]

        # Create a translator object
        translator = Translator(
            from_lang=source_language, to_lang=target_language)

        # Translate the text
        translation = translator.translate(text_to_translate)

        # Send the translated text as a response
        await message.channel.send(translation)

    # Allow other events and commands to be processed
    await bot.process_commands(message)

bot.run(bot_token)
