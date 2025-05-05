import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel is not None:
            message = f"🔊 {member.display_name} подключился к голосовому каналу: {after.channel.name}"
        else:
            message = f"🔇 {member.display_name} вышел из голосового канала: {before.channel.name}"
        send_to_telegram(message)

client.run(DISCORD_TOKEN)
