# 🎮 Gaming Community Discord Bot

A comprehensive Discord bot designed specifically for gaming communities with moderation tools, fun commands, server management features, and utility functions.

## ✨ Features

### 🛡️ Moderation
- **Kick/Ban/Unban** members with reasons
- **Timeout/Mute** functionality with duration
- **Clear/Purge** messages in bulk
- **Warning system** with DM notifications
- **Auto-moderation** for spam and bad words

### 🎯 Server Management
- **Welcome/Goodbye** messages with embed
- **Role management** (add/remove roles)
- **Channel management** (lock/unlock, slowmode)
- **Server setup** commands
- **Mass role operations**

### 🎲 Fun & Gaming
- **Dice rolling** with customizable sides
- **Magic 8-ball** for yes/no questions
- **Trivia games** with questions
- **Rock, Paper, Scissors** gameplay
- **Random user picker**
- **Gaming memes** and compliments
- **Virtual games** (dice game, slot machine)

### 🔧 Utilities
- **Server information** and statistics
- **User profiles** and information
- **Poll creation** with reactions
- **Reminder system** with timeouts
- **Ping/latency** monitoring
- **Bot uptime** tracking
- **Avatar display**

### 📖 Help System
- **Comprehensive help** command
- **Command categorization**
- **Usage examples** and aliases

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)

### 2. Installation

1. **Clone or download** this repository
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables:**
   Create a `.env` file in the root directory and add your Discord bot token:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_CLIENT_ID=your_discord_client_id_here
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

### 3. Discord Setup

1. **Create a Discord Application:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and name it
   - Go to "Bot" section and create a bot
   - Copy the bot token to your `.env` file

2. **Invite Bot to Server:**
   - Go to "OAuth2" > "URL Generator"
   - Select "bot" and "applications.commands" scopes
   - Select required permissions:
     - Administrator (recommended for full functionality)
     - Or individual permissions as needed

3. **Required Permissions:**
   - Send Messages
   - Read Message History
   - Manage Messages
   - Kick Members
   - Ban Members
   - Manage Roles
   - Manage Channels
   - Add Reactions

## 📋 Commands Reference

### Moderation
| Command | Aliases | Description |
|---------|---------|-------------|
| `!kick <member> [reason]` | `!k` | Kick a member |
| `!ban <member> [reason]` | `!b` | Ban a member |
| `!unban <user_id>` | - | Unban a user |
| `!timeout <member> <duration> [reason]` | `!mute` | Timeout a member |
| `!untimeout <member>` | `!unmute` | Remove timeout |
| `!clear [amount]` | `!purge` | Clear messages |
| `!warn <member> [reason]` | `!w` | Warn a member |

### Fun
| Command | Aliases | Description |
|---------|---------|-------------|
| `!roll [sides]` | `!dice, !r` | Roll dice |
| `!8ball <question>` | `!8b, !fortune` | Ask magic 8-ball |
| `!coinflip` | `!flip, !coin` | Flip a coin |
| `!trivia [difficulty]` | `!quiz` | Play trivia |
| `!rps <choice>` | `!rockpaperscissors` | Rock, Paper, Scissors |
| `!meme` | `!funny` | Get a random meme |
| `!compliment [member]` | `!praise` | Give a compliment |
| `!randomuser` | `!randuser, !pick` | Pick random user |
| `!dicegame [bet]` | `!dg` | Play dice game |
| `!slots [bet]` | `!slotmachine` | Play slots |

### Utilities
| Command | Aliases | Description |
|---------|---------|-------------|
| `!serverinfo` | `!si, !guildinfo` | Server information |
| `!userinfo [member]` | `!ui, !whois` | User information |
| `!poll <question> <options...>` | `!vote` | Create a poll |
| `!remind <time> <message>` | `!reminder` | Set reminder |
| `!ping` | `!latency` | Check bot latency |
| `!uptime` | `!up` | Bot uptime |
| `!avatar [member]` | `!pfp` | User avatar |

### Server Management
| Command | Aliases | Description |
|---------|---------|-------------|
| `!setup` | `!init` | Setup server structure |
| `!setwelcome <channel>` | `!welcomeset` | Set welcome channel |
| `!setgoodbye <channel>` | `!goodbyeset` | Set goodbye channel |
| `!roleinfo <role>` | `!ri` | Role information |
| `!channelinfo [channel]` | `!ci` | Channel information |
| `!addrole <member> <role>` | `!ar` | Add role to member |
| `!removerole <member> <role>` | `!rr` | Remove role from member |
| `!slowmode <seconds>` | `!slow` | Set slowmode |
| `!lock [channel]` | `!lockdown` | Lock channel |
| `!unlock [channel]` | `!unlockdown` | Unlock channel |
| `!verify [member]` | `!v` | Verify member |
| `!massrole <role>` | `!mr` | Add role to all |

### Help
| Command | Aliases | Description |
|---------|---------|-------------|
| `!help [command]` | `!h, !commands` | Show help |

## ⚙️ Configuration

Edit `.env` file to customize bot behavior:

```env
# Required
DISCORD_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id_here

# Optional Settings
BOT_PREFIX=!
MONGODB_URI=mongodb://localhost:27017/discord_bot
STEAM_API_KEY=your_steam_api_key
WEATHER_API_KEY=your_weather_api_key

# Gaming Settings
GAMING_ROLE_NAME=Gamer
NEW_MEMBER_ROLE_NAME=Newcomer
VERIFIED_ROLE_NAME=Verified

# Moderation
AUTO_MODERATION=true
SPAM_PROTECTION=true
BAD_WORDS_FILTER=true
WELCOME_CHANNEL_ID=123456789
GOODBYE_CHANNEL_ID=123456789
```

## 🏗️ File Structure

```
server_management_bot/
├── main.py                 # Main bot file
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env                  # Your environment (create manually)
├── cogs/                 # Command categories
│   ├── moderation.py     # Moderation commands
│   ├── fun.py           # Fun and gaming commands
│   ├── utils.py         # Utility commands
│   ├── server_mgmt.py   # Server management
│   └── help.py          # Help system
├── bot.log              # Bot logs (created on first run)
└── README.md            # This file
```

## 🛠️ Advanced Features

### Auto-Moderation
The bot includes automatic moderation features:
- **Spam Protection**: Detects and removes spam messages
- **Bad Word Filter**: Filters inappropriate language
- **Message Length Limits**: Prevents overly long messages

### Database Integration
For advanced features, you can set up MongoDB:
```env
MONGODB_URI=mongodb://localhost:27017/discord_bot
```

This enables:
- Persistent warning system
- User statistics
- Server configuration storage
- Advanced moderation logs

### API Integration
Optional API keys for enhanced features:
- **Steam API**: User profile lookups
- **Weather API**: Weather information

## 🚨 Important Notes

1. **Bot Permissions**: Ensure your bot has the necessary permissions in your Discord server
2. **Rate Limiting**: The bot respects Discord's rate limits
3. **Error Handling**: All commands include proper error handling
4. **Logging**: Bot activities are logged to `bot.log`
5. **Security**: Never share your bot token publicly

## 🆘 Troubleshooting

### Common Issues

1. **Bot not responding:**
   - Check if the bot is running
   - Verify token in `.env` file
   - Check bot permissions

2. **Commands not working:**
   - Verify bot has necessary permissions
   - Check command prefix in config
   - Ensure cogs are loaded properly

3. **Permission errors:**
   - Bot needs higher role than target member
   - Check specific permission requirements

### Getting Help

- Use `!help [command]` for command information
- Check bot logs in `bot.log`
- Ensure all dependencies are installed

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 🔮 Future Enhancements

Planned features:
- Music commands
- Database persistence for all data
- Advanced moderation with reason templates
- Custom command creation
- Server backup/restore
- Integration with popular gaming platforms

---

**Happy Gaming!** 🎮✨
