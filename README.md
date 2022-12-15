# RalseiDiscordBot
A Ralsei discord bot I made and maintained in 2022.

## Why is it so bad?
I made the bot because another (as of writing this) closed-source ralsei bot (https://ralsei.chlod.net/) was going down multiple times every day. And after discord made policy changes with slash commands, it's almost completely dead.
I also (kind of) learned python while making it. The code is horrible, but it "works".
The plan was to have it on one, maybe 2 or 3 servers, but it started to grow... and I don't have the time and resources to maintain it.

## Okay... How do I get it on my discord server?
First of all, you'll need some kind of a server (as in a computer that's running all the time) to host it on. It's not a very resource-intensive program, so something like a Raspberry Pi will absolutely do. 

1. Install [python](https://www.python.org/downloads/) (I tested 3.11) and [py-cord](https://docs.pycord.dev/en/master/installing.html).
2. Downlad this repository, either through the "Download ZIP" option (remember to actually unpack it afterwards!) or by cloning with git.
3. Register a new application in [Discord's developer portal](https://discord.com/developers/applications/), and add a bot to it.
4. Reset the bot token. ___DO NOT___ SHARE IT WITH ANYONE! Instead, put it into a file named `tokenfile.txt`, and put it in the same folder as the files you downloaded in step 2.
5. Open a terminal and navigate to the folder with your files. (Handy tip - On Windows, you can type "cmd" into the address bar, and you'll be done)
6. Start the bot by using `python3 slashsei.py`. If you configured everything correctly, after a few seconds you should see `Logged in as (bot username).`
7. Generate an invite link in the developer portal. For scopes select `bot` and `applications.commands`, and choose your desired permissions.
   - If that sounds too confusing, you can use the following link, just replace the "insert id here" text, with your bot's id, you can find it under the general information tab: https://discord.com/api/oauth2/authorize?client_id=[INSERT_ID_HERE]&permissions=274878172224&scope=bot%20applications.commands 

Afterwards, paste it into a new browser tab.

8. Have fun!
