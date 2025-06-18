# 🤖 Hello-Bot-Discord

A simple, friendly Discord bot that detects sad words and responds with uplifting encouragements. Built with `discord.py`, PostgreSQL, and hosted on platforms like **Render**, **Uptime Robot** and **Neon**.

---

## 🚀 Features

- Responds to sad messages with encouraging words
- Custom **sad words** and **encouragements**
- Toggleable responding mode
- Fun commands like quotes and greetings
- PostgreSQL-based persistent storage

---

## 📜 Commands Guide

### 🤖 Bot Behavior

| Command | Description |
|--------|-------------|
| `$responding true/false` | Enable or disable automatic response to sad words |

> When responding is **ON**, if any word from the *sad words list* is detected in a message, the bot replies with a random *encouragement message*.

---

### ✨ Main Commands

| Command | Description |
|--------|-------------|
| `$hello` | Greet the bot |
| `$quote` | Get a motivational quote from [ZenQuotes API](https://zenquotes.io/api/random) |
| `$addenc <message>` | Add a custom encouragement message |
| `$removeenc <index>` | Remove a custom encouragement by its index |
| `$addsad <word>` | Add a custom sad word |
| `$removesad <index>` | Remove a custom sad word by its index |
| `$list` | Display all encouragements & sad words (default + custom) |
---

**Default Encouragements**:
```
Cheer up!
Hang in there.
You are a great person!
You are great.
I can't even do that, as I'm a Bot.
It is ok
All is well
Good
You are awesome
AWESOME MAN!!
YOU ARE ROCKING!
Great work
Everything is alright
Great people face great failures
Hello how are u
Let it go
Success comes with great failures
The world will be kind to you
You will surely pass this!
```

---

### 😢 Sad Words

**Default Sad Words**:
```
sad, hopeless, depressed, unhappy, angry, depressing, mournful,
despair, misery, miserable, downcast, gloomy, heartbroken,
sorrowful, glum, dispirited, dejected, defeated, woeful,
disheartened, crushed, crestfallen, dismayed, dismal, dreary,
lose, lost, broke, breakup
```

---

## 🛠️ Tech Stack

- Python 3.x
- Flask (for UptimeRobot ping endpoint)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- PostgreSQL (via [Neon](https://neon.tech))
- Hosting via [Render](https://render.com)
- Keep-alive via [Uptime Robot](https://uptimerobot.com)
---

## 💾 Environment Setup (.env) 

```
TOKEN=your_discord_bot_token
DATABASE_URL=your_neon_or_render_postgres_connection_url
```

---

## 🧪 Running Locally

Follow these steps to run the bot on your local machine:

### 1. Clone the repository
```b
git clone https://github.com/your-username/Hello-Bot-Discord.git
cd Hello-Bot-Discord
```
### 2. Create a `.env` file in the root of your project folder with the above Environment Setup

### 3. Create and activate a virtual environment
```
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```
### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Run the bot
```
python main.py
```


## 🧠 Todo / Future Features

- Slash commands (`/`)
- Admin moderation commands
- UI dashboard to manage sad words and encouragements
- Multi-server support with per-server config

