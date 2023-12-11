import youtube_dl
import discord
from discord.ext import commands
import asyncio
import os
import ffmpeg
import math
import re
global TOKEN
from Private import TOKEN
page = 1
msg = ""
PREFIX = '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
message = ""
folder_path = 'C:/Users/georg/Documents/Python/MMMMMusic 1.1/Videos'

file_list = []
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        file_list.append(file_name)

#print(file_list)
#print(colored('hello', 'red'), colored('world', 'green')) #colored text testing


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def reload(ctx):
    file_list = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_list.append(file_name)
    ctx.send("Files reloaded")
    

@bot.command()
async def list(ctx, page=1):
    try:
        page = int(page)
    except ValueError: #handle the error#
        page = 1
    
    pages = math.ceil(len(file_list) / 10) #No partial pages
    msg = ""
    if pages>1:
        for i in range(10): #10 items per message
            msg += str(file_list[i]) + "\n"
        msg += "page " + str(page) + "/" + str(pages)
    elif pages==1: #prevent going out of range
        for i in range(len(file_list)): #amount of files if less than 10
            msg += str(file_list[i]) + "\n"
        msg += "page " + str(page) + "/" + str(pages)
    
    await ctx.send(msg)


@bot.command()
async def play(ctx, url_or_file):
    # Check if the user is in a voice channel
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_channel = ctx.author.voice.channel

    # Connect to the voice channel
    voice_client = await voice_channel.connect()

    # Download audio from the URL or use the file path
    audio_filename = await download_audio(url_or_file)

    # Check if the audio file was obtained successfully
    if audio_filename is None:
        await ctx.send("Failed to obtain the audio.")
        await voice_client.disconnect()
        return

    # Play the audio file
    source = discord.FFmpegPCMAudio(audio_filename)
    voice_client.play(source)

    # Clean up the audio file after playback is finished
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()
    os.remove(audio_filename)

async def download_audio(url_or_file):
    # Check if the given input is a valid URL
    if is_valid_url(url_or_file):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
            }],
            'outtmpl': r'C:\Users\georg\Documents\Python\MMMMMusic 1.1\Videos\%(title)s.%(ext)s',
            'keepvideo': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_or_file, download=False)
                ydl.download([url_or_file])
                audio_filename = ydl.prepare_filename(info)
                return audio_filename
        except youtube_dl.utils.DownloadError:
            return None
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return None
    else:
        # Check if the given input is a valid file path
        if is_valid_file_path(url_or_file):
            return url_or_file
        else:
            return None
def is_valid_url(url):
    # Regular expression pattern to match YouTube URLs
    youtube_regex = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"

    # Check if the URL matches the pattern
    if re.match(youtube_regex, url):
        return True
    else:
        return False

def is_valid_file_path(file_path):
    print("test")
    #file_path_additions = "C:\\Users\\georg\\Documents\\Python\\MMMMMusic 1.1\\Videos\\" + str(file_path)
    #print(file_path_additions)
    # Check if the given file path exists
    #file_path = "C:\\Users\\georg\\Documents\\Python\\MMMMMusic 1.1\\Videos\\test.m4a"
    return os.path.exists(file_path)


"""
@bot.command()
async def help(ctx, cmd):
    if cmd.lower() == "playurl":
        ctx.reply("!playurl")
"""
bot.run(TOKEN)