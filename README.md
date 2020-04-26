# unseen;ninja Bot

Now running with Python. <3

To setup a config.ini for your own instance use the following schema:
```
[bot]
description = your bots description
prefix      = your desired prefix
home_guild  = ID of your main server
log_channel = log channel ID on the main server

[tokens]
discord  = your discord token
unsplash = unsplash API token
```

The unsplash API token is needed for the `bunny` command. If you don't have an API token feel free to remove this line as well as the corresponding line in the `main.py` file and the `bunny` command in `cogs/fun.py`.
