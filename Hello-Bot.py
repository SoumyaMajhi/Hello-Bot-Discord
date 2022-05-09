import discord
import os
import requests
import json
import random
import time
from replit import db
from keep_alive import keep_alive

time.sleep(1) #adds a cooldown of 1 sec

bot = discord.Client()

sad_words = ["sad", "hopeless", "depressed", "unhappy", "angry", "depressing", "mournful", "despair", "misery", "miserable", "downcast", "gloomy", "heartbroken", "sorrowful", "glum", "dispirited", "dejected", "defeated", "woeful", "disheartened", "crushed", "crestfallen", "dismayed", "dismal", "dreary", "lose", "lost", "broke", "breakup"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!",
  "You are great.",
  "I can't even do that, as I'm a Bot."
]    #sentences to show for sad_words

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():      #function for requesting a random quote from the website api
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' ~ ' + json_data[0]['a']
  return(quote)

def update_enc(enc_msg):    #function for updating a new enc msg
  if "enc" in  db.keys():
    enc = db["enc"]
    enc.append(enc_msg)
    db["enc"] = enc
  else:
    db["enc"] = [enc_msg]

def delete_enc(index):    #function for deleting a enc msg
  enc = db["enc"]
  if len(enc) > index:
    del enc[index]
    db["enc"] = enc



@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot)) #shows an opening line in console
  await bot.change_presence(activity=discord.Game(name="with Discord")) #adds a status : Playing with Discord


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  msg = message.content #for shortening

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')   #says hello

  if msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote) #displays a random quote from the website


  if db["responding"]:
    options = starter_encouragements
    if "enc" in db.keys():
      options = options + db["enc"]   #don't completely understand, but i guess it stores the new sentence in the database in options list
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))  #chooses random line from options
      #await message.channel.send(options)


  if msg.startswith("$add"):          #line starting with $new gets added to the options
    enc_msg = msg.split("$add",1)[1]
    update_enc(enc_msg)
    await message.channel.send("New encouraging message added.")


  if msg.startswith("$remove"):  #line starting with $del gets deleted from options
    enc = []
    if "enc" in db.keys():
      index = int(msg.split("$remove",1)[1])
      delete_enc(index)
      enc = db["enc"]
    await message.channel.send(enc)    #shows the remaining lines in options list


  if msg.startswith("$list"):
    enc = []
    if "enc" in db.keys():
      enc = db["enc"] 
    await message.channel.send(enc)

  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is On.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is Off.")

  

#if msg.startswith("$new"):  #was trying another way



keep_alive()

bot.run(os.getenv('TOKEN'))
