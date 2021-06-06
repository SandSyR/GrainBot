import discord
from discord.ext import commands
import os
import requests
import json
import math
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

purge_number = []

#https://stackoverflow.com/questions/55551347/discord-py-i-want-to-grab-a-specific-set-of-numbers-from-a-message-but-im-stu
# Number separator is character between SCP and a number, example with space:
# SCP 1
NUMBER_SEPARATOR = " "
MAXIMUM_SCP_NUMBER = 4999


def get_scp_link(message_content):
    word_list = message_content.split(NUMBER_SEPARATOR)
    scp_number = _extract_scp_number(word_list)
    if scp_number is not None:
        try:
            # int(scp_number) takes care if users already entered 001
            # because it makes it equal to 1
            formatted_number = _format_scp_number(int(scp_number))
            return _build_scp_url(formatted_number)
        except Exception:
            return None


# @param word_list a list of strings
# @return integer or None if error
def _extract_scp_number(word_list):
    captured_scp_number = None

    for index, word in enumerate(word_list):
        if word == "SCP":
            # We're gonna return the word after the current word (index+1)
            # But we have to make sure that the next word exists in the list
            # otherwise we will get IndexError exception
            if index + 1 < len(word_list):
                captured_scp_number = word_list[index + 1]
            else:
                return None
    # If we captured a string in the for loop we have to make sure that that
    # string is actually a number and not some random word example "SCP blabla"
    if captured_scp_number is not None and captured_scp_number.isdigit():
        return captured_scp_number
    return None


# Formats number as a string in format 001-MAXIMUM_SCP_NUMBER
# This allows users to enter 1 instead of 001.
#
# @param number a positive integer to be formatted
# @return string in format 001-MAXIMUM_SCP_NUMBER or raise Exception if error
def _format_scp_number(number):
    if number == 0:
        raise Exception("SCP 0 doesn't exist!")
    elif number > MAXIMUM_SCP_NUMBER:
        raise Exception("SCP number too high! Entry doesn't exist!")
    elif number < 10:
        return "00" + str(number)
    elif number < 100:
        return "0" + str(number)
    else:
        return str(number)

# @param formatted_scp_number a string in format 001-MAXIMUM_SCP_NUMBER
# @return string representing URL to SCP-number web page
def _build_scp_url(formatted_scp_number):
    base_url = "http://www.scp-wiki.net/scp-"
    prefix = "SCP-" + formatted_scp_number + ": "
    return prefix + base_url + formatted_scp_number

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.online, activity=discord.Game('//help'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('//test'):
   await message.channel.send('Test Command Received!')

  if ('69') in message.content:
   await message.channel.send('nice')

  if message.content.startswith('//inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('//clear'):
    if any(word in message.content for word in purge_number):
      purge_number_value = any(word in message.content for word in purge_number)
      await message.channel.purge(limit=purge_number_value)
    else:
      await message.channel.purge(limit=1)

  if "SCP" in message.content:
    scp_link = get_scp_link(message.content)
    if scp_link is not None:
       await message.channel.send(scp_link)

  # @param formatted_scp_number a string in format 001-MAXIMUM_SCP_NUMBER
  # @return string representing URL to SCP-number web page
  def _build_scp_url2(formatted_scp_number):
      if ('SCP-') in message.content:
        base_url = "http://www.scp-wiki.net/scp"
        prefix = "SCP" + formatted_scp_number + ":"
        return prefix + base_url +formatted_scp_number
      else:
        base_url = "http://www.scp-wiki.net/scp-"
        prefix = "SCP-" + formatted_scp_number + ":"
        return prefix + base_url + formatted_scp_number

keep_alive()
client.run(os.environ['TOKEN'])
