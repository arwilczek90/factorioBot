import json
import os
import sys
import time

import boto3
from discord.ext import commands
from sentry_sdk import init, capture_exception, capture_message

if os.environ.get("ENABLE_SENTRY", 'false') == 'true':
    init(os.environ['SENTRY_DSN'])
try:
    access_key = os.environ['ACCESS_KEY']
    secret_key = os.environ['SECRET_KEY']
    print(access_key)
    print(secret_key)
except KeyError as e:
    capture_message('AWS Access keys aren\'t available')
    sys.exit(1)
try:
    instance_id = os.environ["INSTANCE_ID"]
except KeyError as e:
    capture_message('No INSTANCE_ID provided')

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
async def start_server(ctx):
    try:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        instances = describe_response.get('Instances', [])
        for instance in instances:
            if instance.get('State', {}).get('Code') != 80:
                await ctx.send(f'Can\'t stop factorio server as it is in {instance.get("State").get("Name")} state')
                return
        await ctx.send('Starting Factorio Server')
        start_response = client.start_instances(InstanceIds=[instance_id])
        print(json.dumps(start_response))
        await ctx.send(
            'Server Starting, it takes a while to bulid all those blue circuts. '
            '\n I\'ll get back to you with the IP Address in a bit.')
        running = False
        public_ip_address = ''
        while not running:
            describe_response = client.describe_instances(InstanceIds=[instance_id])
            reservations = describe_response.get('Reservations', [])
            for reservation in reservations:
                instances = reservation.get('Instances', [])
                print(len(instances))
                for instance in instances:
                    if instance.get('State', {}).get('Code') == 16:
                        running = True
                        public_ip_address = instance.get('PublicIpAddress')

        await ctx.send(f'Factorio server running at {public_ip_address} . Make The Factory Grow!')
    except Exception as err:
        capture_exception(err)


@bot.command()
async def server_status(ctx):
    try:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        reservations = describe_response.get('Reservations', [])
        for reservation in reservations:
            instances = reservation.get('Instances', [])
            print(len(instances))
            for instance in instances:
                status = instance.get('State', {}).get('Name')
                await ctx.send(f'The server is {status}')
    except Exception as err:
        capture_exception(err)


@bot.command()
async def ip(ctx):
    try:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        reservations = describe_response.get('Reservations', [])
        for reservation in reservations:
            instances = reservation.get('Instances', [])
            print(len(instances))
            for instance in instances:
                if instance.get('State', {}).get('Code') == 16:
                    public_ip_address = instance.get('PublicIpAddress')
                    await ctx.send(f'The server\'s IP Address: {public_ip_address}')
                else:
                    await ctx.send(f'The server isn\'t running please start the server to see its IP Address.')
    except Exception as err:
        capture_exception(err)


@bot.command()
async def stop_server(ctx):
    try:
        describe_response = client.describe_instances(InstanceIds=[instance_id])
        instances = describe_response.get('Instances', [])
        for instance in instances:
            if instance.get('State', {}).get('Code') != 16:
                await ctx.send(f'Can\'t stop factorio server as it is in {instance.get("State").get("Name")} state')
                return
        await ctx.send('Stopping Server Factorio Server')
        start_response = client.stop_instances(InstanceIds=[instance_id])
        print(json.dumps(start_response))
        await ctx.send('Server Stopping by use of artillery')
        running = True
        while running:
            describe_response = client.describe_instances(InstanceIds=[instance_id])
            reservations = describe_response.get('Reservations', [])
            for reservation in reservations:
                instances = reservation.get('Instances', [])
                print(len(instances))
                for instance in instances:
                    if instance.get('State', {}).get('Code') == 80:
                        running = False
            time.sleep(10)

        await ctx.send(f'Factorio server stopped')
    except Exception as err:
        capture_exception(err)


bot.run(os.environ['BOT_TOKEN'])
