# SysStat Discord Bot

A Discord bot that displays real-time system statistics directly inside a Discord channel. SysStat automatically updates a single status message with live CPU, RAM, Disk, and Network usage, complete with a generated graphical dashboard image.

## Features

* 📊 Real-time system monitoring
* 🖥️ CPU usage tracking
* 💾 RAM usage tracking
* 📁 Disk usage tracking
* 🌐 Network usage display
* 🎨 Auto-generated status dashboard image
* 🔄 Automatic updates every 30 seconds
* 📌 Updates a single message instead of spamming channels
* 🟢 Custom bot presence showing system status

## Preview

The bot posts an embedded dashboard containing:

* Current CPU load
* Current RAM load
* Current Disk load
* Network activity
* Visual progress bars
* System online status

## Requirements

* Python 3.9+
* Discord.py
* psutil
* Pillow (PIL)

## Installation

```bash
pip install discord.py psutil pillow
```

## Configuration

1. Create a Discord bot in the Discord Developer Portal.
2. Enable the required intents.
3. Invite the bot to your server.
4. Replace:

```python
TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
STATUS_CHANNEL_ID = STATUS_CHANNEL_ID_HERE
```

with your bot token and target channel ID.

## Run

```bash
python bot.py
```

## Example Use Cases

* Home servers
* VPS monitoring
* Dedicated game servers
* Hosting infrastructure
* Small business systems
* Development environments

## License

MIT License
