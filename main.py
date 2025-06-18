import discord
import os
import requests
import json
import random
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Constants
DEFAULT_SAD_WORDS = [
    "sad", "hopeless", "depressed", "unhappy", "angry", "depressing", "mournful",
    "despair", "misery", "miserable", "downcast", "gloomy", "heartbroken",
    "sorrowful", "glum", "dispirited", "dejected", "defeated", "woeful",
    "disheartened", "crushed", "crestfallen", "dismayed", "dismal", "dreary",
    "lose", "lost", "broke", "breakup"
]

starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person!",
    "You are great.",
    "I can't even do that, as I'm a Bot.",
    "It is ok",
    "All is well",
    "Good",
    "You are awesome",
    "AWESOME MAN!!",
    "YOU ARE ROCKING!",
    "Great work",
    "Everything is alright",
    "Great people face great failures",
    "Hello how are u",
    "Let it go",
    "Success comes with great failures",
    "The world will be kind to you",
    "You will surely pass this!"
]


DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "custom_encouragements": [],
                "custom_sad_words": [],
                "responding": True
            }, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    return json_data[0]['q'] + " ~ " + json_data[0]['a']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="with Discord"))

@bot.event
async def on_message(message):
    global data

    if message.author == bot.user:
        return

    msg = message.content.strip().lower()

    if msg.startswith('$help'):
        help_text = """
    **🤖 Bot Command Help**

    **Encouragements:**
    `$addenc <message>` - Add a custom encouragement  
    `$removeenc <index>` - Remove encouragement by index  
    `$listenc` - Show all custom encouragements

    **Sad Words:**
    `$addsad <word>` - Add a custom sad word  
    `$removesad <index>` - Remove sad word by index  
    `$listsad` - Show all custom sad words

    **Bot Behavior:**
    `$responding true/false` - Turn auto-response on or off

    **Fun:**
    `$hello` - Greet the bot  
    `$quote` - Get a motivational quote

    **Help:**
    `$help` - Show this help message
            """
        await message.channel.send(help_text)
        return


    # Basic Commands
    if msg.startswith('$hello'):
        await message.channel.send('Hello!')

    elif msg.startswith('$quote'):
        await message.channel.send(get_quote())

    elif msg.startswith('$addenc '):
        enc_msg = message.content.split("$addenc", 1)[1].strip()
        data["custom_encouragements"].append(enc_msg)
        save_data(data)
        await message.channel.send("✅ New encouragement added.")

    elif msg.startswith('$removeenc '):
        try:
            index = int(msg.split('$removeenc', 1)[1].strip())
            removed = data["custom_encouragements"].pop(index)
            save_data(data)
            await message.channel.send(f"🗑️ Removed encouragement: {removed}")
        except Exception:
            await message.channel.send("❌ Invalid index. Use `$listenc` to view.")

    # elif msg.startswith('$listenc'):
    #     encs = data["custom_encouragements"]
    #     if encs:
    #         await message.channel.send("📃 Custom encouragements:\n" + "\n".join(f"{i}. {e}" for i, e in enumerate(encs)))
    #     else:
    #         await message.channel.send("No custom encouragements added yet.")

    elif msg.startswith('$list'):
        all_sad = DEFAULT_SAD_WORDS + data["custom_sad_words"]
        all_encs = starter_encouragements + data["custom_encouragements"]

        sad_text = "\n".join(f"{i}. {w}" for i, w in enumerate(all_sad))
        enc_text = "\n".join(f"{i}. {e}" for i, e in enumerate(all_encs))

        response = "**📃 All Sad Words (default + custom):**\n" + sad_text
        response += "\n\n**📃 All Encouragements (default + custom):**\n" + enc_text

        await message.channel.send(response)


    elif msg.startswith('$addsad '):
        word = msg.split("$addsad", 1)[1].strip().lower()
        if word not in data["custom_sad_words"]:
            data["custom_sad_words"].append(word)
            save_data(data)
            await message.channel.send(f"✅ Added new sad word: `{word}`")
        else:
            await message.channel.send(f"`{word}` already exists.")

    elif msg.startswith('$removesad '):
        try:
            index = int(msg.split('$removesad', 1)[1].strip())
            removed = data["custom_sad_words"].pop(index)
            save_data(data)
            await message.channel.send(f"🗑️ Removed sad word: {removed}")
        except Exception:
            await message.channel.send("❌ Invalid index. Use `$listsad` to view.")

    # elif msg.startswith('$listsad'):
    #     sad = data["custom_sad_words"]
    #     if sad:
    #         await message.channel.send("📃 Custom sad words:\n" + "\n".join(f"{i}. {w}" for i, w in enumerate(sad)))
    #     else:
    #         await message.channel.send("No custom sad words yet.")

    elif msg.startswith('$responding'):
        value = msg.split("$responding", 1)[1].strip().lower()
        if value == "true":
            data["responding"] = True
            save_data(data)
            await message.channel.send("✅ Responding is ON.")
        elif value == "false":
            data["responding"] = False
            save_data(data)
            await message.channel.send("🚫 Responding is OFF.")
        else:
            await message.channel.send("Usage: `$responding true` or `$responding false`")

    # Respond to sad messages
    elif data["responding"]:
        all_sad = DEFAULT_SAD_WORDS + data["custom_sad_words"]
        if any(word in msg for word in all_sad):
            all_encs = starter_encouragements + data["custom_encouragements"]
            await message.channel.send(random.choice(all_encs))

bot.run(token)
