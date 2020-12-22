import asyncio
import random
from time import sleep

import discord
import requests
from discord.ext import commands
import logging

from gtts import gTTS

import os
import time

# weird new Intents
# not sure if they are all necessary
intents = discord.Intents().all()
#intents.members = True
#intents.guilds = True
#intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#startup message in console
@bot.event
async def on_ready():
    print("started")

#welcome message
@bot.event
async def on_member_join(member):
    print(f'{member.name} joined the server')
    guild = bot.guilds[0]
    welcome = guild.text_channels[0]
    grl = ['gay rice lickers', 'gays reeking of lust', 'gay retard lovers', 'garlic', 'grandma rodeo league',
           'get rekt lol', 'ginger red ladies', 'great racing lads', 'greatest racers living']

    messages = [f'{member.name} Welcome to hell', f'Welcome {member.name} please don\'t enjoy your stay',
                f'{member.name} Welcome to the shitshow of gяl', f'{member.name} Welcome gяl o/, get your burnt cookies in #shit-talk',
                f'Welcome to Gay Rice lickers, or was it racers? Hmm... Well you\'ll fucking love it here.',
                f'Welcome to gяl where we make fun of everyone.', f'Welcome to ' + random.choice(grl) + ' you\'ll fucking love it here.']
    response = random.choice(messages)
    await welcome.send(response)

#git gud command
@bot.command(name='gg', help= 'Tell someone to git gud')
async def test(ctx, name):
    await ctx.send(f'git gud {name}')

#memes command
@bot.command(name='memes', help='Get popular memes')
async def memes(ctx, number):
    url = 'https://meme-api.herokuapp.com/gimme'

    if int(number) > 5:
        await ctx.send('Please don\'t ask for that many memes')
    else:
        for i in range(int(number)):
            response = requests.request('GET', url)
            data = response.json()
            await ctx.send('{}'.format(data['url']))
            sleep(1)


# insults a grl member
@bot.command(name='insult', help='Insult a grl member')
async def insult(ctx, name):
    insults = open('insults.txt').read().splitlines()
    await ctx.send(f'{name} you {random.choice(insults)}')

async def join(ctx):
   destination = ctx.message.author.voice.channel
   if ctx.me.voice is not None:
     await ctx.me.voice.move_to(destination)
     return

   ctx.me.voice = await destination.connect(timeout = 5)
   await ctx.send(f"Joined {destination} Voice Channel")

# insults a grl member in voice chat
# noinspection SpellCheckingInspection
@bot.command(name='insultvc', help='Insult a grl member in voice chat')
async def insultvc(context, name):
    voice_channel = context.message.author.voice.channel
    if voice_channel is not None:
        # text to speech and save as mp3
        insults = open('insults.txt').read().splitlines()
        audio = gTTS(text=f'{name.replace("@", "")} you {random.choice(insults)}', lang='en', slow=False)
        filename = 'insult-' + str(time.time()) + '.mp3'
        audio.save(filename)

        # connect to vc und play audio
        vc = context.message.author.voice.channel
        currentvc = await vc.connect()
        currentvc.play(discord.FFmpegPCMAudio(filename, options="-loglevel panic"))
        while currentvc.is_playing():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        await currentvc.disconnect()
        os.remove(filename)
    else:
        await context.send(f'Please connect to a voice channel first. You {insult}')

f = open('token.txt', 'r')
token = f.read()
bot.run(token)
