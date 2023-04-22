import discord
import requests

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

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA1NDc3MDE4ODU3NjM1ODQzMA.Gz0NC8.NZZZvc96L9G7DVMtt9Ri2kHaVE1j8cpCT4hC4A')