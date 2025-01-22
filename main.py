import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from converter import VideoDownloader
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')
CLIENT_ID = os.getenv('CLIENT_ID')
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready and connected to Discord.
    Generates and prints an invite link with necessary permissions.
    """
    invite_link = discord.utils.oauth_url(
        CLIENT_ID,
        permissions=discord.Permissions(
            send_messages=True,
            embed_links=True,
            attach_files=True,
            manage_messages=True
        )
    )
    print(f'Bot is ready as {bot.user}')
    print(f'Invite link: {invite_link}')

def is_facebook_video(url):
    """
    Checks if a URL is a Facebook video in any of its formats
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL matches any Facebook video pattern
    """
    facebook_patterns = [
        'fb.watch/',
        'facebook.com/reel/',
        'facebook.com/watch/',
        'facebook.com/story.php',
        'facebook.com/video.php',
        'm.facebook.com/reel/',
        'm.facebook.com/watch/',
        'web.facebook.com/reel/',
        'web.facebook.com/watch/'
    ]
    return any(pattern in url for pattern in facebook_patterns)

def extract_url_and_platform(content):
    """
    Extracts the URL and platform from the message content.
    Flexibly detects URLs from TikTok, Instagram, YouTube, and Facebook
    
    Args:
        content (str): The message content to analyze
        
    Returns:
        tuple: (url, platform) or (None, None) if no valid URL is found
    """
    content = content.strip()
    words = content.split()

    # Check each word for URLs
    for word in words:
        if 'tiktok.com' in word:
            return word, 'tiktok'
        if 'instagram.com' in word and ('/reels/' in word or '/reel/' in word or '/p/' in word):
            return word, 'instagram'
        if 'youtube.com' in word and '/shorts/' in word:
            return word, 'youtube'
        if ('facebook.com' in word or 'fb.watch' in word) and is_facebook_video(word):
            return word, 'facebook'

    return None, None

@bot.event
async def on_message(message):
    """
    Event handler for processing incoming messages.
    Ignores bot messages and commands, processes video URLs if found.
    """
    if message.author.bot or message.content.startswith('!'):
        return

    url, platform = extract_url_and_platform(message.content)
    if url:
        await process_video(message, url, platform)

    await bot.process_commands(message)

async def process_video(message, url, platform):
    """
    Processes a video URL by downloading it and sending it as a Discord message
    with an embedded info card.
    
    Args:
        message (discord.Message): The original message containing the URL
        url (str): The video URL to process
        platform (str): The platform the video is from
    """
    downloader = VideoDownloader()

    try:
        processing_msg = await message.channel.send("\u23f3 Processing video...")

        video_info = await downloader.download_with_info(url)
        if not video_info or not video_info['path']:
            await processing_msg.edit(content="\u274c Could not download the video (possibly too large).")
            return

        video_path = video_info['path']
        info = video_info['info']

        embed = discord.Embed(
            title=info.get('title', 'Video'),
            description=f"Shared by {message.author.mention}\n[View original]({url})",
            color=get_platform_color(platform)
        )

        author_name = info.get('uploader', info.get('channel', 'Unknown'))
        embed.set_author(
            name=f"{platform.capitalize()} \u2022 {author_name}",
            icon_url=message.author.avatar.url if message.author.avatar else None
        )

        duration = info.get('duration', 0)
        duration_str = f"{int(duration)}s" if duration else ""
        quality = info.get('height', '???p')
        info_line = ' \u2022 '.join(filter(None, [
            f"\u26a1 {quality}p" if quality != '???p' else "",
            f"\u23f1 {duration_str}" if duration_str else ""
        ]))

        if info_line:
            embed.add_field(name="", value=info_line, inline=False)

        await processing_msg.edit(content=None, embed=embed)

        with open(video_path, 'rb') as f:
            try:
                await message.channel.send(file=discord.File(f, 'video.mp4'))
                if os.path.getsize(video_path) <= MAX_FILE_SIZE_BYTES:
                    await message.delete()
            except discord.HTTPException:
                await processing_msg.edit(content="\u274c Error sending video: file too large")

        os.remove(video_path)

    except Exception as e:
        await message.channel.send(f"\u274c Error processing video: {str(e)}")
        if 'processing_msg' in locals():
            await processing_msg.delete()

    finally:
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)

def get_platform_color(platform):
    """
    Returns the brand color for different social media platforms
    
    Args:
        platform (str): The platform name
        
    Returns:
        int: Hex color code for the platform
    """
    colors = {
        'tiktok': 0x000000,      # Black
        'instagram': 0xE1306C,    # Instagram Pink
        'youtube': 0xFF0000,      # YouTube Red
        'facebook': 0x1877F2      # Facebook Blue
    }
    return colors.get(platform, 0x7289DA)  # Default Discord color

if __name__ == "__main__":
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    bot.run(TOKEN)