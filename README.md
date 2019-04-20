FactorioBot
===========
This is a small bot to start and stop an instance running factorio.

It is meant to be run on [heroku](https://heroku.com) and can be run for free. And includes basic sentry exception catches
which can be used to catch exceptions in code and is available on heroku for free. However it can be run on anything that is python 3.7 compatible (including windows).

## Environment Variables
* SENTRY_DSN (optional): The DSN for your sentry instance.
* INSTANCE_ID: The instance ID for your factorio server.
* AWS_REGION (optional, default: us-east-1): The region your instance resides in.
* COMMAND_PREFIX (optional, default:$): The Prefix for your bot commands e.g. $start_server
* BOT_TOKEN: Your bot token from discord. [Docs for that can be found here](https://discordpy.readthedocs.io/en/rewrite/discord.html#creating-a-bot-account).
* AWS_ACCESS_KEY_ID (optional if using aws roles or credentials file): Your aws access key id for an IAM user with permissions for the bot.
* AWS_SECRET_ACCESS_KEY (optional if using aws roles or credentials file): Your aws secret access key for an IAM user with permissions for the bot.


## Local Development:

Set your environment variables then:
```
virtualenv venv
pip install -r requirements.txt
python bot.py
```

## Adding to a discord server
follow the docs provided [here](https://discordpy.readthedocs.io/en/rewrite/discord.html#inviting-your-bot)
