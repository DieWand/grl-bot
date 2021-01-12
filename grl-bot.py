import asyncio
import logging
import os
import random
import time
from time import sleep

import discord
import mysql.connector
import requests
import wikipedia
from discord.ext import commands
from gtts import gTTS

# weird new Intents
# not sure if they are all necessary
# probably should only add the ones that we need
intents = discord.Intents().all()

bot = commands.Bot(command_prefix='.', intents=intents)

# init insults and compliments only once
insults = open('insults.txt').read().splitlines()
compliments = open('compliments.txt').read().splitlines()
languages = ['en', 'fr', 'de', 'pl', 'nl', 'fi', 'sv', 'it', 'es', 'pt', 'ru', 'es', 'ja', 'ko', 'no']

# init meanings of grl
grl = ['gay rice lickers', 'gays reeking of lust', 'gay retard lovers', 'garlic', 'grandma rodeo league',
       'get rekt lol', 'ginger red ladies', 'great racing lads', 'greatest racers living']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

'''
f = open('/root/mysqlpw.txt', 'r')
mysqlpw = f.read()
mydb = mysql.connector.connect(
  host="localhost",
  user="grl",
  password=mysqlpw,
  database="grl"
)
mycursor = mydb.cursor(buffered=True)
'''

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

    messages = [f'{member.name} Welcome to hell', f'Welcome {member.name} please don\'t enjoy your stay',
                f'{member.name} Welcome to the shitshow of gяl',
                f'{member.name} Welcome gяl o/, get your burnt cookies in #shit-talk',
                f'{member.name} Welcome to Gay Rice lickers, or was it racers? Hmm... Well you\'ll fucking love it here.',
                f'{member.name} Welcome to gяl where we make fun of everyone.',
                f'{member.name} Welcome to ' + random.choice(grl) + ' you\'ll fucking love it here.']
    response = random.choice(messages)
    await welcome.send(response)
 
'''
#Event adding
@bot.event
async def on_message(message):
    if not message.guild and message.author is not bot.user:
        splitstring = message.content.split()
        if '.addvote' == splitstring[0]:
            if len(splitstring) > 1:
                del splitstring[0]
                questionTableName = ''
                for word in splitstring:
                    questionTableName = questionTableName + word
                question = ''
                for word in splitstring:
                    question = question + word + ' '
                question[:-1]
                if len(questionTableName) >255:
                    await message.channel.send('Your question is too long')
                else:
                    mycursor.execute("USE votes")
                    mycursor.execute(f'CREATE TABLE {questionTableName} (name VARCHAR(255), answer VARCHAR(255))')
                    print('Vote question added')
                    await message.channel.send(f'I added this question to the list: \"{question}\"')
            else:
                await message.channel.send('Please add a question')
                
        if '.vote' == splitstring[0]:
            if len(splitstring) > 1:
                del splitstring[0]

                questiontablename = ''
                for word in splitstring:
                    questiontablename = questiontablename + word

                splitquestion = questiontablename.split(',')
                questiontablename = splitquestion[0]
                vote = splitquestion[1]

                question = ''
                for word in splitstring:
                    question = question + word + ' '
                question[:-1]

                if len(questiontablename) > 255:
                    await message.channel.send('The question is too long')
                else:
                    mycursor.execute("USE votes")
                    mycursor.execute(f'INSERT INTO {questiontablename} (answer) VALUES (\"{vote})\"')
                    mydb.commit()
                    print('Vote added')
                    await message.channel.send(f'I added this vote: \"{vote}\" to the question: \"{question}\"')
            else:
                await message.channel.send('Please add a question')       
'''
                
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
                     
@bot.command(name='tts', help='Let the bot talk for you')
async def tts(context, text, lang='en'):
       await texttospeech(context, text, lang)


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


# ask the bot a question
@bot.command(name='whatis', help='Ask the bot a question.')
async def whatis(context, searchterm):
    await context.send(await getanswer(searchterm))


# noinspection PyBroadException
async def getanswer(searchterm):
    if searchterm == "love":
        return "https://www.youtube.com/watch?v=3rzgrP7VA_Q"
    if searchterm == "grl" or searchterm in grl:
        messages = [f'{random.choice(grl)} is love.',
                    f'{random.choice(grl)} is life.',
                    f'{random.choice(grl)} is the best Trackmania Team that has ever existed.'
                    f'{random.choice(grl)} is a group of beautiful human beeings.',
                    f'{random.choice(grl)} is way better than KSL (Kacke Scheisse League).',
                    f'{random.choice(grl)} is amazing.',
                    f'{random.choice(grl)} is a huge group of very nice dickheads.']
        return random.choice(messages)

    # seach on wikipedia
    try:
        return wikipedia.summary(searchterm, sentences=1)
    except Exception:
        for new_query in wikipedia.search(searchterm):
            try:
                return wikipedia.summary(new_query, sentences=1)
            except Exception:
                pass
    return "I don't know about " + searchterm

# NANINANINANI
@bot.command(name='NANI', help='Step 1: Join voice, Step 2: enjoy Nani, step 3: ??')
async def NANINANINANI(context): 
    await playaudio(context, 1)
        
# bot joins current voice channel, plays the audio file and leaves again
async def playaudio(context, audioID): 
    author = context.message.author
    if audioID == 1: 
        filename == 'NANINANINANI.mp3'
    else if audioID = 2:
        filename = 'having options for later :)' 
        
    if author.voice is not None:
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
