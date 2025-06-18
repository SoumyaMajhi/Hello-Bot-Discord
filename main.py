import discord
import os
import requests
import random
import psycopg2
from dotenv import load_dotenv
from server import keep_alive

# Load environment variables
load_dotenv()
token = os.getenv('TOKEN')
DB_URL = os.getenv('DATABASE_URL')

if not token:
    raise ValueError("TOKEN not set in .env")
if not DB_URL:
    raise ValueError("DATABASE_URL not set in .env")

# PostgreSQL connection
def get_conn():
    return psycopg2.connect(DB_URL)

def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS encouragements (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sad_words (
        id SERIAL PRIMARY KEY,
        word TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS bot_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


# DB operations
def get_encouragements():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT message FROM encouragements")
            return [row[0] for row in cur.fetchall()]

def add_enc(msg):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO encouragements (message) VALUES (%s)", (msg,))
        conn.commit()

def remove_enc(index):
    messages = get_encouragements()
    if index < 1 or index > len(messages):
        raise IndexError(f"Invalid index {index}. Must be between 1 and {len(messages)}.")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM encouragements WHERE id IN (SELECT id FROM encouragements ORDER BY id LIMIT 1 OFFSET %s)",
                (index - 1,)
            )
        conn.commit()

def get_sad_words():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT word FROM sad_words")
            return [row[0] for row in cur.fetchall()]

def add_sad(word):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO sad_words (word) VALUES (%s)", (word,))
        conn.commit()

def remove_sad(index):
    all_sad_words = get_sad_words()
    if index < 1 or index > len(all_sad_words):
        raise IndexError(f"Invalid index {index}. Must be between 1 and {len(all_sad_words)}.")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM sad_words WHERE id IN (SELECT id FROM sad_words ORDER BY id LIMIT 1 OFFSET %s)", 
                (index - 1,)
            )
        conn.commit()

def get_responding():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT value FROM bot_settings WHERE key = 'responding'")
            result = cur.fetchone()
            return result[0] == "true" if result else True  # Default to True if not set

def set_responding(value: bool):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO bot_settings (key, value)
                VALUES ('responding', %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
            """, ("true" if value else "false",))
        conn.commit()

# Static data
DEFAULT_SAD_WORDS = [
    "sad", "hopeless", "depressed", "unhappy", "angry", "depressing", "mournful",
    "despair", "misery", "miserable", "downcast", "gloomy", "heartbroken",
    "sorrowful", "glum", "dispirited", "dejected", "defeated", "woeful",
    "disheartened", "crushed", "crestfallen", "dismayed", "dismal", "dreary",
    "lose", "lost", "broke", "breakup"
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!", "You are great.",
    "I can't even do that, as I'm a Bot.", "It is ok", "All is well", "Good",
    "You are awesome", "AWESOME MAN!!", "YOU ARE ROCKING!", "Great work",
    "Everything is alright", "Great people face great failures",
    "Hello how are u", "Let it go", "Success comes with great failures",
    "The world will be kind to you", "You will surely pass this!"
]

def get_quote():
    resp = requests.get("https://zenquotes.io/api/random").json()
    return resp[0]['q'] + " ~ " + resp[0]['a']

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    init_db()
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="with Discord"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.strip().lower()

    if msg.startswith('$help'):
        help_text = """
**🤖 Bot Command Help**

`$responding true/false` - Toggle auto-responding to sad words

**Encouragements:**
`$addenc <message>` - Add a custom encouragement  
`$removeenc <index>` - Remove encouragement by index  

**Sad Words:**
`$addsad <word>` - Add a custom sad word  
`$removesad <index>` - Remove sad word by index  

**Fun:**
`$hello` - Greet the bot  
`$quote` - Get a motivational quote  
`$list` - Show all encouragements and sad words
        """
        await message.channel.send(help_text)

    elif msg.startswith('$hello'):
        await message.channel.send(f'Hello {message.author.name}!')

    elif msg.startswith('$quote'):
        await message.channel.send(get_quote())

    elif msg.startswith('$addenc '):
        text = message.content.split("$addenc", 1)[1].strip()
        add_enc(text)
        await message.channel.send("✅ Encouragement added!")

    elif msg.startswith('$removeenc '):
        try:
            index = int(message.content.split("$removeenc", 1)[1].strip())
            remove_enc(index)
            await message.channel.send("🗑️ Encouragement removed.")
        except:
            await message.channel.send("❌ Invalid index.")

    elif msg.startswith('$addsad '):
        word = message.content.split("$addsad", 1)[1].strip().lower()
        add_sad(word)
        await message.channel.send(f"✅ Sad word '{word}' added.")

    elif msg.startswith('$removesad '):
        try:
            index = int(message.content.split("$removesad", 1)[1].strip())
            remove_sad(index)
            await message.channel.send("🗑️ Sad word removed.")
        except:
            await message.channel.send("❌ Invalid index.")

    elif msg.startswith('$list'):
        custom_sads = get_sad_words()
        custom_encs = get_encouragements()

        # Prepare text
        default_sads_text = "\n".join(f"{i}. {s}" for i, s in enumerate(DEFAULT_SAD_WORDS))
        custom_sads_text = "\n".join(f"{i}. {s}" for i, s in enumerate(custom_sads))

        default_encs_text = "\n".join(f"{i}. {e}" for i, e in enumerate(starter_encouragements))
        custom_encs_text = "\n".join(f"{i}. {e}" for i, e in enumerate(custom_encs))

        # Combine into final message
        full_message = (
            "**📄 Default Sad Words:**\n" + default_sads_text +
            "\n\n**📝 Custom Sad Words:**\n" + (custom_sads_text or "_None added yet_") +
            "\n\n**📄 Default Encouragements:**\n" + default_encs_text +
            "\n\n**📝 Custom Encouragements:**\n" + (custom_encs_text or "_None added yet_")
        )

        await message.channel.send(full_message)


    elif msg.startswith('$responding '):
        value = message.content.split("$responding", 1)[1].strip().lower()
        if value in ["true", "false"]:
            set_responding(value == "true")
            await message.channel.send(f"✅ Responding set to {value}.")
        else:
            await message.channel.send("❌ Invalid value. Please use `$responding true` or `$responding false`.")

    elif get_responding() and any(word in msg for word in DEFAULT_SAD_WORDS + get_sad_words()):

        all_encs = starter_encouragements + get_encouragements()
        await message.channel.send(random.choice(all_encs))

keep_alive()
bot.run(token)
