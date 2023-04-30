import discord
import requests
import youtube_dl
from discord.ext import commands
import os
from os import system


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors':[{
        'key':'FFmpegExtractAudio',
        'preferredcodec':'mp3',
        'preferredquality':'192',
    }]
}


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
    
    def endSong(guild,path):
        os.remove(path)

    @cat.command(pass_context=True)
    async def play(ctx, url):
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

        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

        await ctx.send(f'**Music: **{url}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('')