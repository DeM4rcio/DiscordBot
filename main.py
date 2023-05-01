import discord
import requests
import youtube_dl
from discord.ext import commands,tasks
import os
from os import system
import asyncio


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
        elif message.content == "?play":
            music = input()
            self.play("play", music)
    
    def endSong(self, guild, path):
        os.remove(path)         

                 
"""
async def play(self, ctx, url):
        if not ctx.message.author.voice:
            await ctx.send('you are not connected to a voice channel')
            return

        else:
            channel = ctx.message.author.voice.channel

        voice_client = await channel.connect()

        guild = ctx.message.guild

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            path = str(file['title']) + "-" + str(file['id'] + ".mp3")

        voice_client.play(url, after=lambda x: self.endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

        await ctx.send(f'**Music: **{url}')
"""
    
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url):
        print(url)
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA1NDc3MDE4ODU3NjM1ODQzMA.GUBWG2.0WCxF-0x7x6JnjHCGFKXvQvFSce-DHOQ5qv7Vg')