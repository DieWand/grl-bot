import asyncio
import logging
import os
import random
import time
from time import sleep

import discord
import requests
from discord.ext import commands
from gtts import gTTS
import mysql.connector

# weird new Intents
# not sure if they are all necessary
# probably should only add the ones that we need
intents = discord.Intents().all()

bot = commands.Bot(command_prefix='.', intents=intents)

# init insults and compliments only once
insults = open('insults.txt').read().splitlines()
compliments = open('compliments.txt').read().splitlines()
languages = ['en', 'fr', 'de', 'pl', 'nl', 'fi', 'sv', 'it', 'es', 'pt', 'ru', 'es', 'ja', 'ko', 'no']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

f = open('/root/mysqlpw.txt', 'r')
mysqlpw = f.read()
mydb = mysql.connector.connect(
  host="localhost",
  user="grl",
  password=mysqlpw,
  database="grl"
)
mycursor = mydb.cursor()


# startup message in console
@bot.event
async def on_ready():
    print("started")


# welcome message
@bot.event
async def on_member_join(member):
    print(f'{member.name} joined the server')
    guild = bot.guilds[0]
    welcome = guild.text_channels[0]
    grl = ['gay rice lickers', 'gays reeking of lust', 'gay retard lovers', 'garlic', 'grandma rodeo league',
           'get rekt lol', 'ginger red ladies', 'great racing lads', 'greatest racers living']

    messages = [f'{member.name} Welcome to hell', f'Welcome {member.name} please don\'t enjoy your stay',
                f'{member.name} Welcome to the shitshow of gяl',
                f'{member.name} Welcome gяl o/, get your burnt cookies in #shit-talk',
                f'{member.name} Welcome to Gay Rice lickers, or was it racers? Hmm... Well you\'ll fucking love it here.',
                f'{member.name} Welcome to gяl where we make fun of everyone.',
                f'{member.name} Welcome to ' + random.choice(grl) + ' you\'ll fucking love it here.']
    response = random.choice(messages)
    await welcome.send(response)
 

#Event adding
@bot.event
async def on_message(message):
    if not message.guild and message.author is not bot.user:
        splitstring = message.content.split()
        if '.vote' == splitstring[0]:
            if len(splitstring) > 1:
                del splitstring[0]
                question = ''
                for word in splitstring:
                    question = question + word + ' '
                if len(word) >255:
                    await message.channel.send('Your question is too long')
                else:
                    mycursor.execute(f'INSERT INTO votes (question) VALUES ({question})')
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
                    await message.channel.send(f'I added this question to the list: \"{question}\"')
            else:
                await message.channel.send('Please add a question')

                
# git gud command
@bot.command(name='gg', help='Tell someone to git gud')
async def test(ctx, name):
    await ctx.send(f'git gud {name}')
    # delete the original message
    await ctx.message.delete(delay=1)

    
# memes command
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
@bot.command(name='insult', help='Insult a grl member.')
async def insult(ctx, name):
    if random.random() < 0.02:
        name = ctx.author.display_name
    await ctx.send(f'{name} you {random.choice(insults)}')
    # delete the original message
    await ctx.message.delete(delay=1)


# insults a grl member in voice chat
@bot.command(name='insultvc', help='Insult a grl member in voice chat. Optional: Language-Tag or "rnd" to randomize '
                                   'the language')
async def insultvc(context, name, lang='en'):
    # get name from mention if exists
    for mentionedmember in context.message.mentions:
        name = mentionedmember.display_name
        break

    if random.random() < 0.02:
        name = context.author.display_name

    if len(name) > 25:
        await context.send(f'Please enter a shorter text you {random.choice(insults)}.')
    else:
        await texttospeech(context, f'{name} you are a {random.choice(insults)}', lang)


# compliment a grl member
@bot.command(name='compliment', help='Compliment a grl member.')
async def insult(ctx, name):
    if 'hammie' in name.lower():
        await ctx.send(f'{name} you are so {random.choice(insults)}')
    else:
        if random.random() < 0.1:
            await ctx.send(f'{name} you are so {random.choice(insults)}')
        else:
            await ctx.send(f'{name} you are so {random.choice(compliments)}')
    # delete the original message
    await ctx.message.delete(delay=1)

    
# compliments a grl member in voice chat
@bot.command(name='complimentvc', help='Compliments a grl member in voice chat. Optional: Language-Tag or "rnd" to '
                                       'randomize the language')
async def complimentvc(context, name, lang='en'):
    # get name from mention if exists
    for mentionedmember in context.message.mentions:
        name = mentionedmember.display_name
        break

    if len(name) > 25:
        await context.send(f'Please enter a shorter text.')
    else:
        if 'hammie' in name.lower():
            await texttospeech(context, f'{name} you are a {random.choice(insults)}', lang)
        else:
            if random.random() < 0.1:
                await texttospeech(context, f'{name} you are a {random.choice(insults)}', lang)
            else:
                await texttospeech(context, f'{name} you are so {random.choice(compliments)}', lang)


# bot joins current voice channel, plays the text via text to speech and leaves again
async def texttospeech(context, text, lang='en'):
    # check if given language is in the list
    if lang != 'rnd' and lang not in languages:
        await context.send(f'Please enter a valid language-tag. These are your options: {*languages,}')
        return

    author = context.message.author
    if author.voice is not None:
        # when language is "rnd", randomize a language
        if lang == 'rnd':
            lang = random.choice(languages)

        # text to speech and save as mp3
        filename = 'tts-' + str(time.time()) + '.mp3'
        audio = gTTS(text=text, lang=lang, slow=False)
        audio.save(filename)

        # connect to vc und play audio           
        vc = author.voice.channel
        currentvc = await vc.connect()
        currentvc.play(discord.FFmpegPCMAudio(filename))
        while currentvc.is_playing():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        await currentvc.disconnect()
        os.remove(filename)
        # delete the original message
        await context.message.delete(delay=1)
    else:
        await context.send(f'Please connect to a voice channel first.')


f = open('/root/token.txt', 'r')
token = f.read()
bot.run(token)
