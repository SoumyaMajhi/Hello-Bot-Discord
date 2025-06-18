# 🤖 Hello-Bot-Discord

A simple, friendly Discord bot that detects sad words and responds with uplifting encouragements. Built with `discord.py`, PostgreSQL, and hosted on platforms like **Render** and **Neon**.

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

### ✨ Encouragements

| Command | Description |
|--------|-------------|
| `$addenc <message>` | Add a custom encouragement message |
| `$removeenc <index>` | Remove a custom encouragement by its index |
| `$list` | Display all encouragements (default + custom) |

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

| Command | Description |
|--------|-------------|
| `$addsad <word>` | Add a custom sad word |
| `$removesad <index>` | Remove a custom sad word by its index |
| `$list` | Display all sad words (default + custom) |

**Default Sad Words**:
```
sad, hopeless, depressed, unhappy, angry, depressing, mournful,
despair, misery, miserable, downcast, gloomy, heartbroken,
sorrowful, glum, dispirited, dejected, defeated, woeful,
disheartened, crushed, crestfallen, dismayed, dismal, dreary,
lose, lost, broke, breakup
```

---

### 🎉 Fun Commands

| Command | Description |
|--------|-------------|
| `$hello` | Greet the bot |
| `$quote` | Get a motivational quote from [ZenQuotes API](https://zenquotes.io/api/random) |

---

## 💾 Environment Setup (.env)

```
TOKEN=your_discord_bot_token
DATABASE_URL=your_neon_or_render_postgres_connection_url
```

---

## 🛠️ Tech Stack

- Python 3.x
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- PostgreSQL (via [Render](https://render.com) or [Neon](https://neon.tech))
- Hosted using [Uptime Robot](https://uptimerobot.com/) + `keep_alive` Flask server

---

## 🧠 Todo / Future Features

- Slash commands (`/`)
- UI dashboard to manage sad words and encouragements
- Multi-server support with per-server config

---

## 🤝 License

MIT License — use freely with love 💙

---

## ✨ Screenshot (optional)

*(Add a Discord screenshot showing the bot in action)*