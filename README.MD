# Social Media Video Discord Bot

A Discord bot that automatically downloads and reposts videos from social media platforms (TikTok, Instagram, YouTube Shorts, and Facebook) directly in Discord channels. The bot handles video compression and size limits automatically to ensure compatibility with Discord's file size restrictions.

## ⚠️ Important Notes

- This bot has been tested only on Windows. While it might work on other operating systems, no testing has been performed.
- This bot is designed for private Discord servers and personal use. It does not include permission checks or rate limiting.
- Use this bot responsibly and respect the terms of service of all platforms.

## ✨ Features

- Automatic video detection from supported platforms
- Video compression for oversized files (using ffmpeg)
- Rich embeds with video information
- Platform-specific color coding
- Original post attribution and links
- Video quality and duration information
- Automatic cleanup of temporary files

## 🎥 Supported Platforms

- TikTok
- Instagram Reels and Posts
- YouTube Shorts
- Facebook Videos and Reels

## 📋 Requirements

- Windows OS (tested only on Windows)
- Python 3.8 or higher
- ffmpeg (for video compression)
- Discord bot token and permissions

## 📥 Step-by-Step Installation Guide

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lazaroagomez/discord-video-downloader-bot.git
   cd discord-video-downloader-bot
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ffmpeg**:
   - Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract the downloaded file
   - Add the ffmpeg `bin` folder to your system's PATH environment variable
   - Verify installation by running: `ffmpeg -version`

5. **Set up the environment variables**:
   - Copy the example environment file:
     ```bash
     copy example.env .env
     ```
   - Edit the `.env` file with your values:
     ```env
     TOKEN=your_discord_bot_token
     CLIENT_ID=your_discord_client_id
     DOWNLOAD_PATH=./downloads
     ```

## 🤖 Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under the bot settings, enable these options:
   - MESSAGE CONTENT INTENT
   - Presence Intent
   - Server Members Intent
5. Copy the bot token and add it to your `.env` file
6. Go to OAuth2 -> General, copy the CLIENT ID and add it to your `.env` file

## 🚀 Running the Bot

1. Make sure your virtual environment is activated:
   ```bash
   .\venv\Scripts\activate
   ```

2. Start the bot:
   ```bash
   python main.py
   ```

3. The bot will print an invite link when it starts. Use this link to invite the bot to your server.

## 📝 Usage

1. Invite the bot to your server using the link it generates on startup
2. Send a supported video URL in any channel
3. The bot will automatically:
   - Download the video
   - Create an embed with video information
   - Compress the video if needed
   - Post the video and embed
   - Clean up temporary files

## 🔑 Required Bot Permissions

The bot needs these permissions to function:
- Send Messages
- Embed Links
- Attach Files
- Manage Messages (for cleaning up original message)

## 🔧 Troubleshooting

Common issues and solutions:

1. **"ffmpeg is not recognized"**:
   - Make sure ffmpeg is properly installed and added to PATH
   - Restart your terminal/IDE after installing ffmpeg

2. **"Error: Cannot find module"**:
   - Make sure you've installed all requirements: `pip install -r requirements.txt`
   - Check that you're in the virtual environment: `.\venv\Scripts\activate`

3. **Videos not downloading**:
   - Check your internet connection
   - Verify the URL is from a supported platform
   - Make sure the video is public/accessible

## 💬 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Create an issue in the GitHub repository with:
   - Detailed description of the problem
   - Steps to reproduce
   - Your operating system and Python version
   - Any error messages you're seeing

## 📄 License

This project is for personal use only. Please respect the terms of service of all platforms involved.

## ⚠️ Disclaimer

This bot is provided as-is, without any guarantees. It's designed for personal use in private Discord servers. Always ensure you have the right to download and share any content.