from asyncio import tasks
import discord 
from discord.ext import tasks
import random
import responses
import os
#import twitch
import yaml

with open("general_configs.yaml","r") as f:
    config = yaml.safe_load(f)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_reponses(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = config['discord']['token']
    client = discord.Client(intents=discord.Intents.all())
    path_input = 'blacklist.properties'
    blacklist = [] 

    if not os.path.isfile(path_input):
        print("Ficheiro inexistente")
    else :
        file = open(path_input, 'r')
    
        for line in file:
            blacklist.append(line.replace('\n',''))
        if not blacklist:
            print("Ficheiro Vazio")
    


    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        #livestreams.start()
        

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        guild = message.guild


        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        for values in blacklist:
            if values in user_message.upper():
                await message.author.add_roles(guild.get_role(575782666121641997))
                await message.delete()
        else:
            await send_message(message, user_message, is_private=False)

    '''
    @client.event
    async def on_message_edit(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)


        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
    '''

    @client.event
    async def on_member_join(member):
        random_role = random.randint(0,3)
        guild = client.get_guild(281505847799054336)
        if random_role == 0:
            await member.add_roles(guild.get_role(471065454576795669))
        elif  random_role == 1:
            await member.add_roles(guild.get_role(471064869781897216))
        elif  random_role == 2:
            await member.add_roles(guild.get_role(471066065116332054))
        elif  random_role == 3:
            await member.add_roles(guild.get_role(471066447330672640))
        
    ''' 
    @tasks.loop(seconds=60)
    async def livestreams():
        channel = client.get_channel(1066026966186201212)
        print(channel)
        streamer = await twitch.get_streamer_status('esquilo1337')
        if streamer :
            #<@&801566186949181441>
            await channel.send(f"https://www.twitch.tv/{streamer.display_name}")
    '''

    
    client.run(TOKEN)