import time
import random
import asyncio
import io
import aiohttp
#pycord
import discord
from discord.ext import commands
#modules
import emotes as e
import responses

#------------------------------------------------------------------------------
#
#       IMPORTANT NOTE:
#       This bot is coded HORRIBLY and inefficently. The only good thing about it, is that it "works".
#       DO NOT use this code, to learn python, or pycord or anything.
#       
#------------------------------------------------------------------------------

tokenfile=open("tokenfile.txt") #preparing the tokenfile
game = discord.Activity(type=discord.ActivityType.listening, name="/")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(activity=game, description="Ralsei Bot", intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


#----------------------------------------------CAKE COMMAND, GROUPHUG, HUG - THE LONG THINGS ---------------------------------------

@bot.slash_command(description="Ralsei bakes a cake.")
async def cake(ctx: discord.ApplicationContext, name: discord.Option(str, "Who is the cake for?",required=0)):
    random.seed()
    mypfp = bot.user.display_avatar.url
    myname = bot.user.display_name
    mypfp = str(mypfp)
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    name = '%0A'.join(name.splitlines())
    #preparing the ingredients
    #start measuring time
    start_time = time.time()
    bakery = ["1 & 1/2 cups of all-purpose flour",
    "1 cup of white sugar","1/2 cup of butter",
    "1/2 cup of milk",
    "1 & 3/4 teaspoons of baking powder",
    "2 eggs",
    "2 teaspoons of vanilla extract"]
    em = discord.Embed(title="Bakery", description="Getting all the ingrdients...",color=discord.Color.dark_green())
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    i=0
    while i<len(bakery):
        em.add_field(name=bakery[i],value=f"❌",inline=False)
        i +=1		
    i=0
    msg = await ctx.respond(embed=em)
    while i<=6:
        em.set_field_at(index=i,name=bakery[i],value=f"✅",inline=False)
        await msg.edit_original_message(embed=em)
        await asyncio.sleep(random.uniform(1,2))
        i +=1
    #mixing
    em = discord.Embed(title="Bakery", description ="Mixing the ingredients...",color=discord.Color.dark_green())
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    await msg.edit_original_message(embed=em)
    await asyncio.sleep(random.uniform(2,5))
    #baking in the oven
    em = discord.Embed(title="Bakery",color=discord.Color.dark_green())
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    readyness=0
    em.add_field(name="🍰 Your cake is baking", value=f"`{readyness*10}%`"+" [⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛]")
    await msg.edit_original_message(embed=em)
    while readyness<10:
        readyness += 1
        await asyncio.sleep(random.uniform(1,3))
        em.set_field_at(0,name="🍰 Your cake is baking", value=f"`{readyness*10}%`"+" ["+readyness*"⬜"+(10-readyness)*"⬛"+"]")
        await msg.edit_original_message(embed=em)
    #taking cake out
    em = discord.Embed(title="Bakery", description ="🍰 Taking out the cake...",color=discord.Color.dark_green())	
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    await msg.edit_original_message(embed=em)	
    await asyncio.sleep(random.uniform(1,2))
    em = discord.Embed(title="Bakery", description ="🍰 Letting the cake cool...",color=discord.Color.dark_green())
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    await msg.edit_original_message(embed=em)
    await asyncio.sleep(random.uniform(4,7))
    #done, stop measuring the time
    em = discord.Embed(title="Bakery", description ="Done!", color=discord.Color.dark_green())
    em.set_author(name=myname+"'s bakery", icon_url=mypfp)
    out = ["https://www.demirramon.com/utgen.png?message=character=trueralsei%20expression=happy%20box=deltarune%20Here%27s%20your%20cake,%20{}.%0AI%20hope%20you%20like%20it!%20",
    "https://www.demirramon.com/utgen.png?message=character=trueralsei%20expression=blush%20box=deltarune%20Here%27s%20your%20cake,%20{}.%0AMay%20I%20have%20a%20slice?%20"]
    em.set_image(url=random.choice(out).format(name))
    elapsed_time = time.time() - start_time
    em.set_footer(text="Baked in "+time.strftime("%M:%S", time.gmtime(elapsed_time)))
    await msg.edit_original_message(embed=em)


@bot.slash_command(description="Hug Ralsei together!")
async def grouphug(ctx: discord.ApplicationContext):
    random.seed()
    channel = ctx.channel.id
    userid = ctx.author
    if userid not in responses.grouphugs:
        name = str(ctx.author.display_name)
        if responses.active_party==channel:
            await ctx.respond("Joined!", delete_after=3)
            responses.grouphugs.append(userid)
        elif responses.active_party!=channel:
            responses.active_party=channel
            await ctx.respond("Come join me and {} for a hug! ❤ \nUse /hug to join, starting in a minute!".format(name))
            responses.grouphugs.append(userid)
            await asyncio.sleep(60) #wait 60 seconds
            hugmess = '{} \n Thank you for the hugs! ❤'
            mentions = [userr.mention for userr in responses.grouphugs]
            huggerlist = "  ".join(mentions)
            await ctx.send(hugmess.format(huggerlist))
            await ctx.send(random.choice(responses.hugart))
            #resetting
            responses.active_party=0
            del responses.grouphugs
            responses.grouphugs = list()


    else:
        await ctx.respond("You already joined!", delete_after=5, ephemeral=True)

#this is awful but it works I guess   

@bot.slash_command(description="Hug ralsei, or join a group hug if one is currently active.")
async def hug(ctx: discord.ApplicationContext, name: discord.Option(str, name="who", description="Who should Ralsei hug? (name/me)",required=0)):
    random.seed()
    channel = ctx.channel.id
    userid = ctx.author
    if responses.active_party==channel: #joining grouphug
        if userid not in responses.grouphugs:
            await ctx.respond("Joined!", delete_after=3)
            responses.grouphugs.append(userid)
        else:
            await ctx.respond("You already joined!", delete_after=5, ephemeral=True) #joining the grouphug
    else:
        if name==None:  #no name given
            name = str(ctx.author.display_name)
            name = name.replace(" ", "%20")
            my_url=(random.choice(responses.gavehug).format(name))
            await ctx.defer()
            async with aiohttp.ClientSession() as session:
                async with session.get(my_url) as resp:
                    if resp.status != 200:
                        return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
                    data = io.BytesIO(await resp.read())
                    await asyncio.sleep(1)
                    await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
        elif name=="me": # self explanatory
            hugme=["https://www.demirramon.com/utgen.png?message=box=deltarune%20character=None%20box=deltarune%20Ralsei%20hugged%20you.%0AYou%20are%20filled%20with%20the%20power%20of%20fluffy%20boys.%20",
            "https://www.demirramon.com/utgen.png?message=box=deltarune%20character=none%20You%20feel%20Ralsei%27s%20soft%20and%20comforting%20hug...%20",
            ]
            my_url=(random.choice(hugme))
            await ctx.defer()
            async with aiohttp.ClientSession() as session:
                async with session.get(my_url) as resp:
                    if resp.status != 200:
                        return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
                    data = io.BytesIO(await resp.read())
                    await asyncio.sleep(1)
                    await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
        else:
            name = name.replace(" ", "%20") # ralsei hugs (name)
            huguser=["https://www.demirramon.com/utgen.png?message=box=deltarune%20character=None%20box=deltarune%20Ralsei%20hugged%20{name}.%0A{name}%20is%20filled%20with%20the%20power%20of%20fluffy%20boys.%20",
            "https://www.demirramon.com/utgen.png?message=box=deltarune%20character=none%20{name}%20felt%20Ralsei%27s%20soft%20and%20comforting%20hug...%20"]
            my_url=(random.choice(huguser).format(name=name))
            await ctx.defer()
            async with aiohttp.ClientSession() as session:
                async with session.get(my_url) as resp:
                    if resp.status != 200:
                        return await ctx.send('The textbox generator is down. {}'.format(e.bruh))
                    data = io.BytesIO(await resp.read())
                    await asyncio.sleep(1)
                    await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
#TODO: ADD more RESPONSES

#----------------------------------------GREETINGS, GOODBYES - TEXTBOX GENERATORS WITH A NAME-----------------------------------
@bot.slash_command(description="Ralsei greets you, or anyone else!")
async def greetings(ctx: discord.ApplicationContext, name: discord.Option(str, description="Who should Ralsei say hi to? ",required=0)):
    random.seed()
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.greetings).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))

@bot.slash_command(description="Good morning!")
async def morning(ctx: discord.ApplicationContext, name: discord.Option(str, description="Who should Ralsei say good morning to? ",required=0)):
    random.seed()
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.morning).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))


@bot.slash_command(description="Goodnight!")
async def night(ctx: discord.ApplicationContext, name: discord.Option(str, description="Who should Ralsei say goodnight to? ",required=0)):
    random.seed()
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.night).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))

@bot.slash_command(description="Goodbye!")
async def goodbye(ctx: discord.ApplicationContext, name: discord.Option(str, description="Who should Ralsei say goodbye to? ",required=0)):
    random.seed()
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.bye).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
    #done
@bot.slash_command(description="Ralsei encourages you (or anyone else).")
async def encourage(ctx: discord.ApplicationContext, name: discord.Option(str, name="who", description="Who should Ralsei encourage? ",required=0)):
    random.seed()
    if name == None:
        name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.encouragements).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
    #done

#-----------------SHORT RESPONSES-------------------

@bot.slash_command(description="Give ralsei a diet coke.")
async def dietcoke(ctx: discord.ApplicationContext):
    random.seed()
    name = str(ctx.author.display_name)
    name = name.replace(" ", "%20")
    my_url=(random.choice(responses.dietcoke).format(name))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))

@bot.slash_command(description="Ralsei will answer your wacky questions.")
async def ask(ctx: discord.ApplicationContext, question: discord.Option(str, name="question", description="What would you like to ask? ",required=1)): # yes, the questions mean absolutely nothing to the bot.
    random.seed()
    my_url=(random.choice(responses.answers))
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))

@bot.slash_command(description='Play deltarune ch.1-7 on discord!')
async def deltarune(ctx: discord.ApplicationContext):
	await ctx.respond("""```❌Fatal error. Currently, Discord is not a supported platform.
Deltarune is available on PC/Mac through Steam/itch.io, Playstation 4 and Nintendo Switch.```""")

@bot.slash_command(description='Merry Christmas!')
async def krismas(ctx: discord.ApplicationContext):
	await ctx.respond("https://tenor.com/view/krismas-gif-24100809")

@bot.slash_command(description='Ralsei Not Safe For Work')
async def nsfw(ctx: discord.ApplicationContext):
	await ctx.respond('https://twitter.com/Cw1tchy/status/1484554750628892672')    

@bot.slash_command(description='Do some moves')
async def dance(ctx: discord.ApplicationContext):
	random.seed()
	await ctx.respond(random.choice(responses.dance))

@bot.slash_command(description='Art with ralsei giving or receiving hugs.')
async def hugs(ctx: discord.ApplicationContext):
	random.seed()
	await ctx.respond(random.choice(responses.hugart))


#-----------------------------------------OTHER TEXTBOX STUFF---------------------------------------

@bot.slash_command(description="Generate a textbox. For names and expressions visit: bit.ly/boxgen")
async def say(ctx: discord.ApplicationContext, 
text: discord.Option(str, name="text", description="The text of the message.",required=1),
character: discord.Option(str, description="The character that will say whatever you'd like. Can be set to none.",required=0),
expression: discord.Option(str, description="The character's expression. The default will be used if not specified.",required=0),
animate: discord.Option(str, description="Should the text be animated?",required=0,choices=["True"])
):

    if animate=="True": 
        gentext="https://www.demirramon.com/utgen.gif?message=box=deltarune%20animate=true%20"
        fileformat="gif"
    else: 
        gentext="https://www.demirramon.com/utgen.png?message=box=deltarune%20"
        fileformat="png"
    text = '%0A'.join(text.splitlines())
    if character!=None and expression!=None:
        text = gentext+"character={}%20expression={}%20".format(character,expression) + text.replace(" ", "%20") + "%20"
    elif character!=None:
        text = gentext+"character={}%20".format(character) + text.replace(" ", "%20") + "%20" 
    elif expression!=None:
        text = gentext+"character={}%20expression={}%20".format("trueralsei",expression) + text.replace(" ", "%20") + "%20"
    else:
        text = gentext+"character=trueralsei%20" + text.replace(" ", "%20") + "%20" 
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(text) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.{}'.format(random.getrandbits(16),fileformat)))

@bot.slash_command(description="Generate a link for a textbox. Use /say unless you know what you're doing.")
async def sayl(ctx: discord.ApplicationContext, 
text: discord.Option(str, name="text", description="The text of the message.",required=1),
character: discord.Option(str, description="The character that will say whatever you'd like. Can be set to none.",required=0),
expression: discord.Option(str, description="The character's expression. The default will be used if not specified.",required=0),
animate: discord.Option(str, description="Should the text be animated?",required=0,choices=["True"])
):

    if animate=="True": 
        gentext="https://www.demirramon.com/utgen.gif?message=box=deltarune%20animate=true%20"
    else: 
        gentext="https://www.demirramon.com/utgen.png?message=box=deltarune%20"
    text = '%0A'.join(text.splitlines())
    if character!=None and expression!=None:
        text = gentext+"character={}%20expression={}%20".format(character,expression) + text.replace(" ", "%20") + "%20"
    elif character!=None:
        text = gentext+"character={}%20".format(character) + text.replace(" ", "%20") + "%20" 
    elif expression!=None:
        text = gentext+"character={}%20expression={}%20".format("trueralsei",expression) + text.replace(" ", "%20") + "%20"
    else:
        text = gentext+"character=trueralsei%20" + text.replace(" ", "%20") + "%20" 
    await ctx.defer()
    await ctx.respond(text)

@bot.slash_command(description='Ask Ralsei to choose from a list of things, seperated by "or".')
async def choose(ctx: discord.ApplicationContext, 
text: discord.Option(str, name="list", description='What are our options? Remember, seperate them with "or".',required=1)):
    if text == "" or " or " not in text:
        await ctx.respond("I didn't get that, could you ask again?")
    else:
        text = text.split(" or ")
        choice = random.randint(0,(len(text) - 1))
        my_url=(random.choice(responses.chose).format(text[choice].replace(" ", "%20")))
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                if resp.status != 200:
                    return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
                data = io.BytesIO(await resp.read())
                await asyncio.sleep(1)
                await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))


#---------------------------------------------------------------------THE RIGHT CLICK THINGY----------------------------------------------
@bot.message_command(name="Make this a textbox!")
async def messtobox(ctx: discord.ApplicationContext, message: discord.message):
    avatar=message.author.display_avatar.url.replace(" ","%20")
    text=message.clean_content
    text=text.replace(" ","%20")
    text = '%0A'.join(text.splitlines())
    my_url=("https://www.demirramon.com/utgen.png?message=box=deltarune%20character=custom%20url="+avatar+"%20"+text+"%20")
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))


@bot.message_command(name="Make this an animated textbox!")
async def messtoabox(ctx: discord.ApplicationContext, message: discord.message):
    avatar=message.author.display_avatar.url.replace(" ","%20")
    text=message.clean_content
    text=text.replace(" ","%20")
    text = '%0A'.join(text.splitlines())
    my_url=("https://www.demirramon.com/utgen.gif?message=box=deltarune%20animate=true%20character=custom%20url="+avatar+"%20"+text+"%20")
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.respond('The textbox generator is down. {}'.format(e.bruh))
            data = io.BytesIO(await resp.read())
            await asyncio.sleep(1)
            await ctx.respond(file=discord.File(data, 'textbox{}.gif'.format(random.getrandbits(16)))) 
#--------------------------------LISTENERS - adding reactions and other trash------------------------------------------

@bot.listen()
async def on_message(message):
    msgun = message.content.lower()
    channel = message.channel
    msg = msgun.replace(" ", "")
    noreply = ["```","shutupbot"]

   	#rule34 replies
    rule = ['bodypillow','rule34','r34','e621','porn','nsfw']
    chars = ('toriel','sans','flowey','papyrus','undyne','alphys','mettaton','asgore','asriel','tem','temmie','monsterkid','dummy','napstablook','muffet','gaster','frisk','chara','kris',
        'noelle','berdly','queen','rouxls','kaard','spamton','susie','trashy','jevil','tasque','lancer','starwalker','ralsei','nubert', 
        'heats flamesman', 'cornby', 'froggit')
    if any(word in msg for word in rule) and any(word in msgun for word in chars) and "```" not in msg:
        await message.add_reaction(e.gun)
        await message.add_reaction(e.gun2)
        await message.add_reaction(e.gun3)
        my_url=('https://www.demirramon.com/utgen.png?message=box=deltarune%20character=custom%20url=https://cdn.discordapp.com/attachments/959412636913639444/965685106037653514/unknown.png%20Stop.%20') #ralsei with a gun.
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                if resp.status != 200:
                    return await channel.send('The textbox generator is down. {}'.format(e.bruh))
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
        
    if any(word in msg for word in noreply):
        pass
    else:
        #sleep replies
        sleep = ['1am','2am','3am','4am','5am','6am']
        notsleep = ['11am','12am']
        if any(word in msg for word in sleep):
            if not any(word in msg for word in notsleep):
                my_url=('https://www.demirramon.com/utgen.png?message=character=custom%20url=https://cdn.discordapp.com/attachments/960637718054981645/965499190924968007/unknown.png%20expression=happy%20box=deltarune%20Go%20the%20fuck%20to%20sleep.%20') #the image is morgana from persona 5, if that ever goes missing.
                async with aiohttp.ClientSession() as session:
                    async with session.get(my_url) as resp:
                        if resp.status != 200:
                            return await channel.send('The textbox generator is down. {}'.format(e.bruh))
                        data = io.BytesIO(await resp.read())
                        await channel.send(file=discord.File(data, 'textbox{}.png'.format(random.getrandbits(16))))
                

    		#egg reactions
        if 'egg' in msgun:
            await message.add_reaction(e.eggsei)
            
            #ball reactions
        if 'ball' in msgun:
            await message.add_reaction(e.ballsei)
            
            #plushie reactions
        plush = ['larsey','plush','Rarusei']
        if any(word in msgun for word in plush):
            random.seed()
            await message.add_reaction(random.choice(e.plush))
            
            #spamton
        spamtong = ['bigshot','spamton','[[']
        if any(word in msg for word in spamtong):
            random.seed()
            await message.add_reaction(e.spamtong)
            
            #badbot reactions
        if 'badbot' in msg:
            await message.add_reaction(e.gun2)
            
            #mlao
        mlao = ['mlao','lmao','potassium','banana']
        if any(word in msgun for word in mlao):
            await message.add_reaction(e.mlao)
            
    		#pog
        if 'pog' in msgun:
            await message.add_reaction(e.pog)
            
            #blunt
        weed = ['weed','drug','blunt','smoke','doobie','richsei']
        if any(word in msgun for word in weed):
            random.seed()
            await message.add_reaction(random.choice(e.blunt))
            
        #babey		
        if 'babey' in msgun:
            await message.add_reaction(e.babey)
            await message.add_reaction('🅱')
            await message.add_reaction('🇦')
            await message.add_reaction('🇧')
            await message.add_reaction('🇪')
            await message.add_reaction('🇾')
            
            #jevil x spamton, don't ask.
        if 'jevilxspamton' in msg or 'spamtonxjevil' in msg:
            await message.add_reaction(e.yes)	
            
        #the mess i like to call the shipping thing
        if any(word in msg for word in chars):
            potential_ship = msg.split("x")
            n=1
            while n < len(potential_ship):
                if potential_ship[n-1].endswith(chars) and potential_ship[n].startswith(chars):
                    await message.add_reaction('🛳')
                    
                    break
                else:
                    n +=1

bot.run(tokenfile.read())
