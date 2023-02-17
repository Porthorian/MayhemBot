#!/usr/bin/env python3

import discord
import re
import logging
import string
import os
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s|%(levelname)s|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

BOT_TOKEN = open('bot_token', 'r').read()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    logging.debug(f'We have logged in as {client.user}')

@tree.command(name = "cuck_count", description = "How many cucks have been said leaderboard")
async def get_cuck_count(interaction):
    data_map = {}
    logging.info('Getting Cuck Count')
    async for msg in interaction.channel.history(limit=10000):
        if msg.author == client.user: continue

        count = len(re.findall(r'cuck', msg.content))
        if count >= 1:
            if msg.author not in data_map:
                data_map[msg.author] = 0

            data_map[msg.author] += count

    logging.debug('Size of Leaderboard: %s' % len(data_map))
    if len(data_map) < 1:
        return
    
    sorted_list = sorted(data_map.items(), key=lambda item: item[1])
    message = ''
    counter = 0
    for row in sorted_list:
        counter += 1
        user = row[0].name
        cuck_count = row[1]
        message += "%s. %s - %s\n" % (counter, user, cuck_count)
    message = message.rstrip(string.whitespace)
    logging.debug("Sending Message \n%s" % message)
    await interaction.response.send_message(message)
    logging.debug('Message Sent')


client.run(BOT_TOKEN)