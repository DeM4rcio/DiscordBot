import discord
import youtube_dl
from discord.ext import commands,tasks
import os
import asyncio
from dotenv import load_dotenv




ytdl_format = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    } 

ffmpeg_options = {
    'options':'-vn'
}

load_dotenv()
DISCORD_TOKEN = os.getenv('pip install os-sys')

ytdl = youtube_dl.YoutubeDL(ytdl_format)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

"""
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == "?regras":
            await message.channel.send(f'{message.author.name} não enche o saco, estou em manutenção.');
        elif message.content == "?sigaa":
            url = 'https://sigaa.unb.br/'
            if requests.get(url).status_code == 200:
                await message.channel.send(f'Sigaa disponível!'+ "\u2705");
            else:
                await message.channel.send(f"Sigaa indisponivel"+"\u1F7E5")
"""

    
   


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



@bot.command(name = 'join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return 
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()



@bot.command(name= 'play')
async def play(ctx,url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url,loop=bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable="C:\WORKSPACE\Python\Discord_bot\ffmpeg",source=filename))
    await ctx.send(f'**Now Playing:**{filename}')



@bot.command(name='pause')
async def pause(ctx):
    voice_cliente = ctx.message.guild.voice_client
    if voice_cliente.is_playing():
        await voice_cliente.pause()
    else:
        await ctx.send("Pausa porque não tem música!")



@bot.command(name='resume')
async def resume(ctx):
    voice_cliente = ctx.message.guild.voice_client
    if voice_cliente.is_paused():
        await voice_cliente.resume()
    else:
        await ctx.send("O bot não está tocando!")



@bot.command(name='leave')
async def leave(ctx):
    voice_cliente = ctx.message.guild.voice_client
    if voice_cliente.is_connected():
        await voice_cliente.disconnect()
    else:
        await ctx.send("o bot não ingressou em um canal de voz! ")



@bot.command(name='stop')
async def resume(ctx):
    voice_cliente = ctx.message.guild.voice_client
    if voice_cliente.is_playing():
        await voice_cliente.stop()
    else:
        await ctx.send("O bot não está tocando nada!")




#client = MyClient(intents=intents)
if __name__ == "__main__":
    bot.run("MTA1NDc3MDE4ODU3NjM1ODQzMA.GgXU95.EMka3-IGFhlPKBBWFANZ7np3cvDPWtjfShdR-Q")
