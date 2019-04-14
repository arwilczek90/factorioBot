import time

import discord
import os
import json
import sys
import boto3
from discord.ext import commands

try:
    access_key = os.environ['ACCESS_KEY']
    secret_key = os.environ['SECRET_KEY']
    print(access_key)
    print(secret_key)
except KeyError as e:
    print('AWS Access keys aren\'t available')
    sys.exit(1)
try:
    instance_id = os.environ["INSTANCE_ID"]
except KeyError as e:
    print('No INSTANCE_ID provided')

bot = commands.Bot(command_prefix='$')
client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")


@bot.command()
async def startServer(ctx):
    await ctx.send('Starting Factorio Server')
    start_response = client.start_instances(InstanceIds=[instance_id])
    print(json.dumps(start_response))
    ctx.send('Server Starting, it takes a while to bulid all those blue circuts. \n I\'ll get back to you with the IP Address in a bit.')
    running = False
    public_ip_address = ''
    while not running:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        instances = describe_response.get('Instances', [])
        for instance in instances:
            if instance.get('State', {}).get('Code') == 16:
                running = True
                public_ip_address = instance.get('PublicIpAddress')

    await ctx.send(f'Factorio server running at {public_ip_address} . Make The Factory Grow!')

@bot.command()
async def stopServer(ctx):
    await ctx.send('Starting Factorio Server')
    start_response = client.stop_instances(InstanceIds=[instance_id])
    print(json.dumps(start_response))
    ctx.send('Server Stopping by use of artillery')
    running = True
    while running:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        instances = describe_response.get('Instances', [])
        for instance in instances:
            if instance.get('State', {}).get('Code') == 80:
                running = False
        time.sleep(10)

    await ctx.send(f'Factorio server stopped')


bot.run(os.environ['BOT_TOKEN'])
