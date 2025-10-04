import discord
from discord.ext import commands, tasks
import os
import asyncio
import datetime
import re
import random
import json

from keep_alive import keep_alive
from setup import get_settings, update_settings, get_status, update_status, get_channels, update_channels, get_channel, update_channel, clean_channels


token = os.environ['TOKEN']
client = commands.Bot(command_prefix="", chunk_guilds_at_startup=False, self_bot=True)
client.remove_command("help")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


def sorted_channels():
    channels = get_channels()
    s = sorted(list(channels), key=lambda c: channels[c]["Position"])
    return s

def paginate(temp_list, maxchars=1800):
    size = 0
    message_text = []
    for item in temp_list:
        if len(item) + size > maxchars:
            yield message_text
            message_text = []
            size = 0
        message_text.append(item)
        size += len(item)
    yield message_text

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    if get_status()["Running"] is True:
        waifu.start()
        print('> Activated')

    
@tasks.loop()
async def kl(channel):
    await channel.send("$kl 10")
    try:
        await client.wait_for("message", timeout=2, check=lambda m: m.channel==channel and "You need an additional" in m.content)
        kl.cancel()
    except asyncio.TimeoutError:
        pass
        
                              
@client.event
async def on_reaction_add(reaction, user):

    if user == client.user and str(reaction.emoji) == "⏹️":
        kl.cancel()
        
@client.event
async def on_message_edit(message1, message2):

    #Claim logger
    try:
        if message1.author.id == 432610292342587392:
            embed2 = message2.embeds[0]
            embed1 = message1.embeds[0]
            desc = embed2.description.replace("\n", "\n=> ")
            if f"Belongs to {client.user.name}" in embed2.footer.text and "roulette* · " not in embed2.description and embed2 != embed1:
                with open("claimed.txt", 'a', encoding='utf-8') as claimed:
                    claimed.write(f"= {datetime.datetime.now()}\tClaim Success!\n= {message1.channel.name}\n=> {embed2.author.name}\n==> {desc}\n\n")
                    print("Claim logged")

    except:
        return False


@client.event
async def on_message(message):
    mauthor = message.author
    cuser = client.user
    mcontent = message.content
    mstart = mcontent.startswith
    try:
        mchannel = message.channel
    except:
        return
    try:
        msend = mchannel.send
    except:
        return
        
    mreact = message.add_reaction
    mcid = mchannel.id
    channels_dict = get_channels()
    channels = list(channels_dict)

    from_mudae = mauthor.id == 432610292342587392
    
    if from_mudae and f"**{cuser.name}**" in mcontent:
        print("Found tu")
        global check_tu
        def check_tu(channel_id):
            print(f"Checking tu... \nLast tu channel: {mchannel.id} \nRequired Channel: {channel_id}")
            if mcid == channel_id:
                return message
            else: 
                return None

    if cuser.mentioned_in(message) and from_mudae:
        if "wants to give you" in mcontent:
            await asyncio.sleep(5)
            async with mchannel.typing():
                await asyncio.sleep(0.5)
                await msend("y")
            await asyncio.sleep(2)
            async with mchannel.typing():
                await asyncio.sleep(1.5)
                await msend("thx")
            pass
            
    
    '''

    spammers = [971702227024613396, 947077202627944448]

    
    #Needs update
    #*Move to a cog
    if cuser.mentioned_in(message) and "TextChannel" in str(message):
        if mcontent == "" or mauthor.id in spammers:
            return
        if mauthor != cuser:
            notifier = await client.fetch_user(940603435093463121)
            mid = str(message.id)
            ref = str(message)
            if "TextChannel" in ref:
                mguild = message.guild
                mgid_str = str(mguild.id)
                text = f"🔔 **{mauthor}:** \
                \n{mcontent}\
                \n \
                \n> **Server: `{mguild}`**\
                \n> **Channel: `{mchannel.name}`** \
                \n> https://discord.com/channels/{mgid_str}/{mcid}/{mid}"
                await notifier.send(text)

    if 'DMChannel' in str(message):
        if mauthor != cuser:
            notifier = await client.fetch_user(940603435093463121)
            mid = message.id
            text = f"👤 **{mauthor}:** \
            \n{mcontent}\
            \n \
            \n> **Direct Message**\
            \n> https://discord.com/channels/@me/{mcid}/{mid}"
            await notifier.send(text)
    '''

    if mauthor != cuser:
        return

    if mstart(",pos "):
        split = mcontent.split(" ")
        po = int(split[1])
        for item in channels_dict:
        
            if channels_dict[item]["Position"] == po:
                i = int(split[2]) -1
                channels_sorted = sorted_channels()
                j = channels_sorted.index(item)
                print(i, j)
                if j>i:
                    channels_sorted.insert(i,channels_sorted.pop(j))
                elif j<=i:
                    channels_sorted.insert(i+1,channels_sorted[j])
                    del channels_sorted[j]
                for index, channel in enumerate(channels_sorted):
                    p = index + 1
                    channels_dict[channel]["Position"] = p
                update_channels(channels_dict)
                
                await mreact("☑️")
                break
    

    if mstart(",debug"):
        print(f"yes")

    if mstart("$kakeraloot 10"):
        kl.start(mchannel)    

    #Needs update
    #*remove db repetition to improve speed
    if mstart(",show"):
        if len(channels) != 0:
            lines = []
            for channel_key in sorted_channels():
                channel_settings = get_channel(channel_key)
                position = channel_settings["Position"]
                kpmax = channel_settings["KPMax"]
                kpcons = channel_settings["KPCons"]
                kpthresh = channel_settings["KPThresh"]
                char_thresh = channel_settings["CharThresh"]
                claim_thresh = channel_settings["ClaimThresh"]
                if channel_settings["ButtonsToggle"] is True:
                    buttons = "B: 🔷"
                elif channel_settings["ButtonsToggle"] is False:
                    buttons = "B: 🔶"
                if channel_settings["ButtonsClaimer"] is True:
                    buttonsc = "Bc: 🔷"
                elif channel_settings["ButtonsClaimer"] is False:
                    buttonsc = "Bc: 🔶"
                if channel_settings["Slash"] is True:
                    slash = "S: 💚"
                elif channel_settings["Slash"] is False:
                    slash = "S: 💔"
                channel = client.get_channel(int(channel_key))
                text = f"Channel {position}: **{channel.name}** ({channel.guild})\n> [{kpcons}/{kpmax}]\n> [ChT: **{char_thresh}** | ClT: **{claim_thresh}**]\n> [KPT: {kpthresh}]\n> [{slash}]\n> [{buttons} | {buttonsc}]"
                lines.append(text)
                
            for message_text in paginate(lines):
                text = "\n".join(message_text)
                await msend(text)
        else:
            await msend('No Channel set yet.')

    #activate
    if mstart(",act"):
        status = get_status()
        status["Running"] = True
        update_status(status)
        waifu.start()
        print('> Activated')
        await mreact("🔄")

    if mstart(",react"):
        stopper()
        await asyncio.sleep(0.5)
        waifu.start()
        print("> Reactivated")
        await mreact("🔄")

    #stop
    if mstart(",stop"):
        status = get_status()
        status["Running"] = False
        update_status(status)
        stopper()
        print('> Stopped')
        await message.add_reaction("🛑")

    #Check setting and status
    if mstart(",stat"):
        status = get_status()
        tmin = status["Minute"]
        if status["Running"] is True:
            zrun = "on"
        elif status["Running"] is False:
            zrun = "off"
        text = f"> Exact minute set to __**xx:{tmin}**__ [Status **__{zrun}__**]"
        await msend(text)

    #Purge set channels
    if mstart(",clean"):
        clean_channels()
        print("Clean successful")

    #Changes the roll minute. Ex: ",rim 42" (rolls in minute 42)
    if mstart(",rim "):
        status = get_status()
        status["Minute"] = mcontent.split(" ")[1]
        tmin = status["Minute"]
        update_status(status)
        print(f"Timer set to: xx:{tmin}")
        await mreact("☑️")      

    #Changing kakthreshold. Will be multiplied to kakera power consumption. The roller prevents kakera power from going below the threshold when deciding if it should react to yellow. Ex: "$tu t 2" (Default)
    if mstart("$llik "):
        try:
            channel_settings = get_channel(mcid)
            channel_settings["KPThresh"] = int(mcontent.split(" ")[1])
            t = channel_settings["KPThresh"]
            update_channel(mcid, channel_settings)
            print(f"New kp thresh for {mchannel.name}: {t}")
            await asyncio.sleep(2)
            await msend("$kr")
        except ValueError:
            return
            
    if mstart("$alea 00"):
        try:
            channel_settings = get_channel(mcid)
            channel_settings["ClaimThresh"] = int(mcontent.split(" 00")[1])
            t = channel_settings["ClaimThresh"]
            update_channel(mcid, channel_settings)
            print(f"New claim thresh for {mchannel.name}: {t}")
            await asyncio.sleep(2)
            await msend("$kt")
        except ValueError:
            return
                     
    if mstart("$alea 01"):
        try:
            channel_settings = get_channel(mcid)
            channel_settings["CharThresh"] = int(mcontent.split(" 01")[1])
            t = channel_settings["CharThresh"]
            update_channel(mcid, channel_settings)
            print(f"New char thresh for {mchannel.name}: {t}")
            await asyncio.sleep(2)
            await msend("$kt")
        except ValueError:
            return

    #Remove channel
    if mstart("$tu r"):
        if str(mcid) in channels:
            channels = get_channels()
            del channels[str(mcid)]
            channels_sorted = sorted(list(channels), key=lambda c: channels[c]["Position"])
            for index, channel in enumerate(channels_sorted):
                p = index + 1
                channels[str(channel)]["Position"] = p
            update_channels(channels)
            #Just for confirmation
            await asyncio.sleep(2)
            await msend("$kr")
            

    #Adding channel
    if mstart("$tu a"):
        if str(mcid) not in channels:
            position = len(get_channels()) + 1
            default = {
                "Position": position,
                "KPMax": None,
                "KPCons": None,
                "KPThresh": 50,
                "ButtonsToggle": False,
                "ButtonsClaimer": False,
                "ClaimThresh": 400,
                "CharThresh": 270,
                "Slash": True
            }
            update_channel(str(mcid), default)
            print(f"Added {mchannel.name}")
            await asyncio.sleep(2)
            #Triggering to update KPMax and KPCons to the right values
            await msend("$bonus a")

    #Updating max kakera power and kakera power consumption for channel
    if mstart("$bonus a"):
        def check_bonus_message(bmessage):
            return bmessage.author.id == 432610292342587392 and "Player Bonuses" in bmessage.content
        if str(mcid) in channels:
            try:
                bonus = await client.wait_for("message", timeout=2, check=check_bonus_message)
                kpmax, kpcons = parse_bonuses(bonus.content)
                channel_settings = get_channel(mcid)
                channel_settings["KPMax"] = kpmax
                channel_settings["KPCons"] = kpcons
                update_channel(mcid, channel_settings)
                print(f"{mchannel.name}: Successfully set KPMax to {kpmax} and KPCons to {kpcons}")
            except asyncio.TimeoutError:
                print("Couldn't find bonus message")
                return

    #Changing channel position to given position. Ex "$tu p 3"
    if mstart("$llba "):
        split = mcontent.split(" ")
        i = int(split[1]) -1
        channels_sorted = sorted_channels()
        j = channels_sorted.index(str(mcid))
        if j>i:
            channels_sorted.insert(i,channels_sorted.pop(j))
        elif j<=i:
            channels_sorted.insert(i+1,channels_sorted[j])
            del channels_sorted[j]
        for index, channel in enumerate(channels_sorted):
            p = index + 1
            channels_dict[str(channel)]["Position"] = p
        update_channels(channels_dict)

    #Kill script, for dupes
    if mcontent == ",abort":
        def check(message):
            return message.author.id == client.user.id and message.content == "confirm"
        await message.reply("Send \"confirm\" to abort", mention_author=False)
        message = await client.wait_for("message", timeout=45.0, check=check)
        await message.reply("Shutting down...", mention_author=False)
        os._exit(0)

    #Reloading cogs. Ex: ",reload claimlist"
    if mstart(",reload "):
        extension = mcontent.split(" ")[1]
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        print(f"Reloaded extension {extension}")

    #$mmabt 2 for all buttons,
    #$mmabt 1 if regular unclaimed doesnt have buttons
    #$mmabf 1 if no buttons
    if mstart("$llab"):
        channel_settings = get_channel(mcid)
        if "f" in mcontent:
            channel_settings["ButtonsToggle"] = False
        elif "t" in mcontent:
            channel_settings["ButtonsToggle"] = True
        if "o-" in mcontent:
            channel_settings["ButtonsClaimer"] = False
        elif "o+" in mcontent:
            channel_settings["ButtonsClaimer"] = True
        update_channel(mcid, channel_settings)

    if mstart("$wls"):
        channel_settings = get_channel(mcid)
        if "f" in mcontent:
            channel_settings["Slash"] = False
        elif "t" in mcontent:
            channel_settings["Slash"] = True
        update_channel(mcid, channel_settings)

    if mstart(",roll"):
        print("Rolling...")
        global indx
        indx = 0
        await starter(wa.start)

    if mstart("$tu s"):
        wa.cancel()
  

######################################################

# Roller
                
######################################################


    

async def check_traffic(channel):
    print("Checking traffic...")
    
    while True:
        try:
            await client.wait_for("message", timeout=4, check=lambda msg: msg.channel == channel and msg.author.id == 432610292342587392)
            continue
        except asyncio.TimeoutError:
            break

def prep():
    print(indx + 1)
    channel_id = int(sorted_channels()[indx])
    channel = client.get_channel(channel_id)
    tu_attempts = 0
    return channel_id, channel, tu_attempts
    
def stopper():
    wa.cancel()
    waifu.cancel()
    char_claimer.cancel()
    kak_claimer.cancel()
    wish_claimer.cancel()

async def starter(wa_mode):
    global indx
    sorted_keyl = sorted_channels()
    
    async def tu_loop(wa_mode, channel_id, channel, tu_attempts):
        global indx
        
        while True:
            tu_attempts += 1
            
            print(f"[{channel.name}]")
            await check_traffic(channel)
    
            print("All clear!")

            # Send tu
            await channel.send("$tu")
            
            await asyncio.sleep(2)

            tu_message = check_tu(channel_id)


            if tu_message is None:
                if tu_attempts == 3:
                    print("Tu can't be fount... Going to next channel")
                    indx += 1
                    return False
                else:
                    await asyncio.sleep(3)
                    continue
                    
            roll_amount, can_claim, next_claim, can_rt, kp, can_dk, can_daily, next_rolls = parse_tu(tu_message.content)
            await asyncio.sleep(1)
            if roll_amount - 1 == 0:
                print("Looks like we're already done there")
                indx += 1
                return False
            if can_daily is True:
                await channel.send("$daily")
            channel_settings = get_channel(channel.id)
            kp_max = channel_settings["KPMax"]
            kp_cons = channel_settings["KPCons"]
            kpthresh = channel_settings["KPThresh"]
            tbuttons = channel_settings["ButtonsToggle"]
            claimbuttons = channel_settings["ButtonsClaimer"]
            claim_thresh = channel_settings["ClaimThresh"]
            char_thresh = channel_settings["CharThresh"]
            slash = channel_settings["Slash"]
            kak_claimer.start(channel, kp, kp_max, kp_cons, can_dk, kpthresh, tbuttons)
            wish_claimer.start(channel, tbuttons)
            char_claimer.start(channel, can_claim, can_rt, next_claim, next_rolls, tbuttons, claimbuttons, claim_thresh, char_thresh)
            print("Commencing wa...")
            print(roll_amount)
            try:
                wa_mode(channel, roll_amount, slash)
            except RuntimeError:
                wa.cancel()
                await asyncio.sleep(1)
                wa.start(channel, roll_amount, slash)
                break
            return True



    done = False
    while True:
        if done is True:
            break
        elif indx < len(sorted_keyl):
            channel_id, channel, tu_attempts = prep()
            done = await tu_loop(wa_mode, channel_id, channel, tu_attempts)
        else: 
            indx = None
            break


  
      
@tasks.loop(minutes=60)
async def waifu():
    print("> Started rolling")
    global indx
    indx = 0
    await starter(wa.start)

async def min_limroul(channel):
    await asyncio.sleep(15)

    at = 0
    while True:
        at+=1
        try:
            lim = await channel.send("$limroul 1 1 1 1")
            await asyncio.wait([client.wait_for("reaction_add", check=lambda r, u: u.id == 432610292342587392 and r.message == lim), 
                                client.wait_for("message", check=lambda m: m.author.id == 432610292342587392 and ("gamemode" in m.content))
                               ],
                              return_when=asyncio.FIRST_COMPLETED,
                              timeout=2
                              )
            break
        except asyncio.TimeoutError:
            if at >= 3:
                break
            continue

@tasks.loop()
async def wa(channel, roll_amount, slash):

        
    #Determined if it sends slash or not, used by char claimer
    global get_expire
     
    intervals = [2,1.7, 1.6, 1.5, 1.4, 1.3, 1.8, 1.9,5,2,1.7, 1.6, 1.5, 1.4, 1.3, 1.8, 1.9,2,1.7, 1.6, 1.5, 1.4, 1.3, 1.8, 1.9]
    await asyncio.sleep(random.choice(intervals))
    
    while True:
        if wish_claim_pause() is True or claim_pause() is True:
            print(f"Wish claim pause: {wish_claim_pause()}")
            print("Roll paused...")
            await asyncio.sleep(2)
            continue
        else:
            break
            
    if roll_amount >= wa.current_loop+1 == roll_amount-3:
        if limroul():
            await channel.send("$limroul 100000 100000 100000 100000")
            asyncio.ensure_future(min_limroul(channel))
            await asyncio.sleep(0.5)
          
    """async with channel.typing():"""

    
    try:
        raise
        if not slash:
            raise
        async for command in channel.slash_commands(query="wa"):
            if command.name == "wa":
                await command() 
                def get_expire():
                    return 87
    except:
        await channel.send('$waifua うちにおいでs') 
        def get_expire():
            return 43
    
    if wa.current_loop == roll_amount-1:
        wa.stop()
    
        
@waifu.before_loop
async def wait_until():
    
    now = datetime.datetime.now()
    print(now)
    next_run = now.replace(minute= int(get_status()["Minute"]), second=0)

    if next_run < now:
        next_run += datetime.timedelta(hours= 1)
        
    print(next_run)
    await discord.utils.sleep_until(next_run)


@wa.after_loop
async def switch_channel():
    global indx
    char_claimer.cancel()
    kak_claimer.cancel()
    wish_claimer.cancel()
    indx += 1
    await starter(wa.restart)



######################################################

# Claimers
                
###################################################### mudae



@tasks.loop(count=1)
async def kak_claimer(channel, kp, kp_max, kp_cons, can_dk, thresh, buttons):

    kaks = ['<:kakeraW:608192076286263297>', '<:kakeraL:815961697918779422>', '<:kakeraO:605112954391887888>',  '<:kakeraR:605112980295647242>','<:kakeraY:605112931168026629>','<:kakeraP:609264156347990016>']
    kakY = '<:kakeraY:605112931168026629>'
    kakP = '<:kakeraP:609264156347990016>'
    

    just_dked = False
    cons = kp_cons
    #Waiting for kakera spaawn in channel
    
    if buttons is True:
        def check_kak_spawn(message):
            try: 
                return str(message.components[0].children[0].emoji) in kaks and message.channel == channel
            except:
                return False
        kmessage = await client.wait_for("message", check=check_kak_spawn)
        kemoji = str(kmessage.components[0].children[0].emoji)
        async def ktake():
            await asyncio.sleep(0.2)
            await kmessage.components[0].children[0].click()
            
    elif buttons is False:
        def check_kak_spawn(reaction, user):
            return reaction.message.channel == channel and user.id == 432610292342587392 and str(reaction.emoji) in kaks
        kak, user = await client.wait_for("reaction_add", check=check_kak_spawn)
        kmessage = kak.message
        kemoji = str(kak.emoji)
        async def ktake():
            await kmessage.add_reaction(kemoji)

        
    kembed = kmessage.embeds[0]

    #Check if half_react
    if "chaoskey" in kembed.description and f"Belongs to {client.user.name}" in kembed.footer.text:
        cons //= 2

    #DK if kakera is detected and current kakera power is less than kak consumption
    if kp < cons and kemoji != kakP and can_dk is True:
        csend = channel.send
        cwait = client.wait_for
        def check_dk_success(dkmessage):
            return ("added to your kakera" in dkmessage.content or "Next $dk reset" in dkmessage.content) and dkmessage.channel == channel
        #Retry and retry dk until confirmation or cooldown message is recieved
        while True:
            await asyncio.sleep(0.2)
            await csend("$dk")
            try: 
                dkmessage = await cwait("message", timeout=2, check=check_dk_success)
                if "added to your kakera" in dkmessage.content:
                    can_dk = False
                    kp = kp_max
                    just_dked = True
                    print("DK success")
                    print(f"KP = {kp}")
                    break
                else:
                    can_dk = False
                    break
            except asyncio.TimeoutError:
                continue

    if kemoji != kakY:
        #Try to take regardless of kakera power because why not
        await ktake()
        print(kemoji)
        #Now calculate if it should subtract
        if kp >= cons and kemoji != kakP:
            kp -= cons
            print(f"KP = {kp}")

    elif kemoji == kakY:
        #Yellow kakera should not make kakera power dip below threshold, unless dk is ready
        kpconsed = kp - cons
        if (can_dk is True and kp >= cons) or (can_dk is False and kpconsed >= thresh) or just_dked is True:
            await ktake()
            print(kemoji)
            kp -= cons
            print(f"KP = {kp}")

    kak_claimer.restart(channel, kp, kp_max, kp_cons, can_dk, thresh, buttons)



@tasks.loop()
async def wish_claimer(channel, buttons):

    global wish_claim_pause
    pause = False
    
    def wish_claim_pause():
        return pause
        
    print(f"Wish claim pause: {wish_claim_pause()}")

    cwait = client.wait_for
    cuser = client.user
    cmentioned = cuser.mentioned_in
    asyncio_ensure = asyncio.ensure_future

    print("Wish Claimer Started")

    
    #Defining function for claiming wish
    async def wish_claimer_inner(wish_spawn):
    
            if buttons is False:
                try:
                    def check_wish_reaction(reaction, user):
                        return user.id == 432610292342587392 and wish_spawn == reaction.message
                    wish_reaction, user = await cwait("reaction_add", timeout=2, check=check_wish_reaction)
                    wremoji = str(wish_reaction.emoji)
                    async def wtake():
                        await wish_spawn.add_reaction(wremoji)
            
                except asyncio.TimeoutError:
                    print("Uhh whoops, we lost the wish")
                    return
                    
            elif buttons is True:
                
                async def wtake():
                    await asyncio.sleep(0.2)
                    await wish_spawn.components[0].children[0].click()
            
            await wtake()

            
            try:
                def check_success(message1, message2):
                    return message1 == wish_spawn
        
                await cwait("message_edit", timeout=2, check=check_success)
                print("Claimed wish successfully")
            except asyncio.TimeoutError:
                nonlocal pause
                
                pause = True
                print(f"Wish claim pause: {wish_claim_pause()}")
                if buttons is False:
                    await wish_spawn.remove_reaction(wremoji, cuser)
    
                #retries $rt if cooldown message or rt confirmation is received
                while True:
                    print("Trying to rt...")
        
                    def check_rt_fail(cd_message):
                        return "cooldown" in cd_message and cd_message.author.id == 432610292342587392 and cd_message.channel == channel
                    
                    await asyncio.sleep(0.2)
                    rtmessage = await channel.send("$rt")
        
                    confirm, fail = await asyncio.gather(
                        cwait("reaction_add", timeout=1, check=lambda rtreaction, user: rtreaction.message == rtmessage and user.id == 432610292342587392),
                        cwait("message", timeout=1, check=check_rt_fail),
                        return_exceptions=True
                    )
                    print(f"rt confirm: {confirm}\nrt fail: {fail}")
    
                    if isinstance(confirm, asyncio.TimeoutError) and not isinstance(fail, asyncio.TimeoutError):
                        print("Can't RT")
                    
                    elif not isinstance(confirm, asyncio.TimeoutError) and isinstance (fail, asyncio.TimeoutError):
                        print("RTed! Claiming wish...")
                    
                    elif isinstance(confirm, asyncio.TimeoutError) and isinstance(fail, asyncio.TimeoutError):
                        continue
                    
                    break

                await wtake()
                pause = False
                print(f"Wish claim pause: {wish_claim_pause()}")

    #Check for wish
    def check_wish(message):
        return "Wished by" in message.content and cmentioned(message) and message.author.id == 432610292342587392 and message.channel == channel
        
    #Wait for wish
    wish_spawn = await cwait("message", check=check_wish)

    #Firing it separately so it can loop back to detecting wishes
    asyncio_ensure(wish_claimer_inner(wish_spawn))

    

@tasks.loop(count=1)
async def char_claimer(channel, can_claim, can_rt, next_claim, next_rolls, tbuttons, claimbuttons, claim_thresh, char_thresh):

    global claim_pause
    global limroul
    pause = False
    def claim_pause():
        return pause
    #Couldn't think of a cleaner way to pass values to char_claimer.afterloop
    global get_claimer_values

    def get_claimer_values():
        return char_likedg, series_wishedg, series_likedg, unclaimed_spawn, channel, next_claim, next_rolls, can_claim, can_rt, claimbuttons
    
    #Reading json
    with open("cogs/List.json", "r") as f:
        jsondict = json.load(f)

    #Looking for global likelist in json file
    llglobal = jsondict["LikelistGlobal"]
    lgchars = llglobal["Characters"]
    lgseries = llglobal["Series"]

    #Looking for global wishlist in json file
    wlglobal = jsondict["WishlistGlobal"]
    wgchars = wlglobal["Characters"]
    wgseries = wlglobal["Series"]

    #Looking for channel wishlist in json file
    try:
        wishlist = jsondict[f"Wishlist{channel.id}"]
        wchars = wishlist["Characters"]
        wseries = wishlist["Series"]
    except KeyError:
        wchars = []
        wseries = []

    blacklist = jsondict["BlacklistGlobal"]
    blacklistchars = blacklist["Characters"]
    blacklistseries = blacklist["Series"]

    #Lists to append spawn to. Prioriizes accordingly: liked chara, wished series, liked series, any unclaimed spawn
    char_likedg = []
    series_wishedg = []
    series_likedg = []
    unclaimed_spawn = []

    def limroul():
        nchars = len(unclaimed_spawn) + len(series_likedg) + len(series_wishedg) + len(char_likedg)
        return nchars == 0 and next_rolls == next_claim and can_claim

    csend = channel.send
    cmentioned = client.user.mentioned_in
    asyncio_ensure = asyncio.ensure_future

    cwait = client.wait_for

    def check_spawn(spawn_message):
        try:
            sembed = spawn_message.embeds[0]
            return spawn_message.author.id == 432610292342587392 and spawn_message.channel == channel and "Belongs to" not in sembed.footer.text and "roulette*" not in sembed.description
        except:
            return False

    async def char_claimer_inner(spawned):
        nonlocal pause
        
        #Checking for react, then taking the reaction
        if claimbuttons or ("Wished" in spawned.content and tbuttons is True):
            emoji = None
            async def claimer(s, e=None):
                await asyncio.sleep(0.2)
                await s.components[0].children[0].click()
                
        elif not claimbuttons:
            try:
                reaction, user = await cwait("reaction_add", timeout=1, check=lambda r, u: r.message == spawned and u.id == 432610292342587392)
                emoji = str(reaction.emoji)
            except asyncio.TimeoutError:
                emoji = "💠"
            async def claimer(s, e):
                await s.add_reaction(e)
                    
    
        now = datetime.datetime.now()
        roll_time = [int(now.day), int(now.hour), int(now.minute), int(now.second), int(now.microsecond)]

        
        spawn_embed = spawn.embeds[0]
        name, series, val, claim_rank = parse_spawn(spawn_embed)

        if channel.id == 873147584464711712 and claim_rank is not None:
            if claim_rank <= 400:
                return
            print(f"Passed claim rank check (rank = {claim_rank})")
                

        nonlocal can_claim, can_rt
        #If user had it wished, just leave it to wish claimer and update claim and rt availability
        if cmentioned(spawned):
            if can_claim:
                can_claim = False
            elif can_rt:
                pause = True
                can_rt = False
                await asyncio.sleep(4)
                pause = False
            return

        elif name in blacklistchars or series in blacklistseries:
            return
                
        #Check if character is in wishlist
        elif name in wchars or name in wgchars or series in wseries or val >= claim_thresh:
            if can_claim:
                await claimer(spawned, emoji)
                can_claim = False
            elif can_rt is True:
                pause = True
                await asyncio.sleep(0.3)
                rt_message = await csend("$rt")
                try:
                    await cwait("reaction_add", timeout=1, check=lambda r, u: r.message == rt_message and u.id == 432610292342587392)
                    can_rt = False
                except asyncio.TimeoutError:
                    rt_message = await csend("$rt")
                    can_rt = False
                    try:
                        await cwait("reaction_add", timeout=1, check=lambda r, u: r.message == rt_message and u.id == 432610292342587392)
                    except asyncio.TimeoutError:
                        pass
                await claimer(spawned, emoji)
                pause = False
            return


        elif can_claim is False and val <= char_thresh:
            return

        s = get_expire()

        char_info = {"Spawn_id": f"{spawn.id}", "Value": val, "Time": roll_time, "Claimer": claimer, "Emoji": emoji, "Expire": s}
            
        if name in lgchars:
            print(f"+Liked Character\n>Name: {name}\n=Series: {series}")
            char_likedg.append(char_info)

        elif series in wgseries:
            print(f"+Wished Series\n>Name: {name}\n=Series: {series}")
            series_wishedg.append(char_info)
            
        #Will add to possible claims if value is more than 270
        elif next_claim != next_rolls and val <= char_thresh:
            return
            
        elif series in lgseries:
            print(f"+Like Series\n>Name: {name}\n=Series: {series}")
            series_likedg.append(char_info)

        else:
            print(f"+Unclaimed\n>Name: {name}\n=Series: {series}")
            unclaimed_spawn.append(char_info)
            

        
    print("Char claimer started")
    while True:
        #Waiting for unclaimed spawn
        spawn = await cwait("message", check=check_spawn)
        print("Unclaimed Spawn Detected")
        asyncio_ensure(char_claimer_inner(spawn))



@char_claimer.after_loop
async def claimer():

    #Taking values from char_claimer
    char_likedg, series_wishedg, series_likedg, unclaimed_spawn, channel, next_claim, next_rolls, can_claim, can_rt, claimbuttons = get_claimer_values()

    print("Char Claimer canceled")

    sorted_value = sorted(char_likedg + series_wishedg + series_likedg + unclaimed_spawn, key=lambda x: x["Value"], reverse=True)
    
    def find_highest_value():
        for chara_dict in sorted_value:
            dtnow = datetime.datetime.now
            val = chara_dict["Value"]
            t = chara_dict["Time"]
            expr = chara_dict["Expire"]
            print(f"highest = {val}")
            dtnow = datetime.datetime.now
            roll_time = dtnow().replace(day=t[0], hour=t[1], minute=t[2], second=t[3], microsecond=t[4])
            tdiff = dtnow() - roll_time 
            if tdiff < datetime.timedelta(seconds=expr):
                return val
        return None


    #Chooses what to claim after the roll is over. Picks from liked characters spawned, then liked series spawned and lastly just takes whatever isn't claimed (prioritizes the highest valued in each list), Also makes sure that it the spawn isn't past 42 seconds. (45 is the spawn expiration, usually)
    async def claimer_inner():
        
        for spawn_list in [char_likedg, series_wishedg, series_likedg, unclaimed_spawn]:
            if len(spawn_list) > 0:
                sorted_prio = sorted(spawn_list, key=lambda x: x["Value"], reverse=True)
                
                async def picker():
                    nonlocal can_claim
                    for spawn_prio in sorted_prio:
                        
                        val = spawn_prio["Value"]
                        spawn_id = spawn_prio["Spawn_id"]
                        emoji = spawn_prio["Emoji"]
                        expr = spawn_prio["Expire"]
                        print(f"{spawn_id}, {val}")
    
                        if val != 0:
                            hval = find_highest_value()

                            if hval is not None:
        
                                print(hval-val)
                                #if there's a huge difference with highest value claimable, skip
                                if hval - val > 150:
                                    continue
                                    
    
                        print("Passed value check")
                        t = spawn_prio["Time"]
                        dtnow = datetime.datetime.now
                        roll_time = dtnow().replace(day=t[0], hour=t[1], minute=t[2], second=t[3], microsecond=t[4])
                        nspawn = await channel.fetch_message(int(spawn_id))
                        tdiff = dtnow() - roll_time 
                        if tdiff < datetime.timedelta(seconds=expr):
                            if can_claim is True:
                                await spawn_prio["Claimer"](nspawn, emoji)
                                can_claim = False
                                print(f"Claimed {nspawn.embeds[0].author.name} in {channel.name}")
                                return False
                            elif can_rt is True and tdiff < datetime.timedelta(seconds=expr) and val > 270:
                                csend = channel.send
                                cwait = client.wait_for
                                rt_message = await csend("$rt")
                                try:
                                    await cwait("reaction_add", timeout=1, check=lambda r, u: r.message == rt_message and u.id == 432610292342587392)
                                except asyncio.TimeoutError:
                                    rt_message = await csend("$rt")
                                    try:
                                        await cwait("reaction_add", timeout=1, check=lambda r, u: r.message == rt_message and u.id == 432610292342587392)
                                    except asyncio.TimeoutError:
                                        pass
                                await spawn_prio["Claimer"](nspawn, emoji)
                                return True
                            elif can_rt is False:
                                return True
                    return False
                    
                done = await picker()
                print("Passed Picker")
                if done is True:
                    break
                print("Not done... Next List")

    asyncio.ensure_future(claimer_inner())
            
    
    

######################################################

# Parsers
                
######################################################

def parse_spawn(spawn_embed):

    desc = spawn_embed.description

    #Character Name
    char_name = spawn_embed.author.name

    #Look for series name
    match = re.search(r'^(.*?[^\n]*)', desc, re.DOTALL)
    if match:
        char_series = match.group(1).replace('\n', ' ').strip()

    #Look for value, if none just put it as 0
    match = re.search(r'(?<=\*\*)(\d+)', desc, re.DOTALL)
    if match:
        char_val = int(match.group(0))
    elif match is None:
        char_val = 0

    #
    #remove when stuff is claimed on maso server
    match = re.search(r'(?<=Claims:\ #)(\d+)', desc)
    if match: 
        claim_rank = int(match.group(0))
    elif match is None:
        claim_rank = None

    return char_name, char_series, char_val, claim_rank
        

def parse_bonuses(bonus_content):

    #Max Kakera Power
    kpmax = re.search(r"Kakera max power.*?(\d+)", bonus_content)
    kpmax = int(kpmax.group(1))

    #Kakera power consumption
    kpcons = re.search(r"Power cost.*?(\d+)", bonus_content)
    kpcons = int(kpcons.group(1))

    return kpmax, kpcons

def parse_tu(tu_content):

    #Roll amount
    match = re.search(r"You have.*?(\d+).*?rolls", tu_content)
    roll_amount = int(match.group(1)) + 1

    match = re.search(r"\+.*?(\d+).*?\$us", tu_content)
    if match:
        roll_amount += int(match.group(1))

    print(f"Roll amount = {roll_amount - 1}")

    #Can claim
    match = re.search(r"(__can__|can't) claim.*?(\d+(?:h\ \d+)?)", tu_content)
    if match.group(1) == "__can__":
        can_claim = True
    elif match.group(1) == "can't":
        can_claim = False

    print(f"Can claim = {can_claim}")

    #Next claim
    if "h " in match.group(2):
        time = match.group(2)
        h = time.split("h ")[0]
        m = time.split("h ")[1]
    else:
        h = 0
        m = match.group(2)
    next_claim = datetime.datetime.now() + datetime.timedelta(hours=int(h), minutes=int(m))
    next_claim = str(next_claim.month)+ "_" + str(next_claim.day) + "_" + str(next_claim.hour) + "_"+ str(next_claim.minute)

    print(f"Next claim = {next_claim}")
    
    #Next rolls
    match = re.search(r"Next rolls.*?(\d+(?:h\ \d+)?)", tu_content)
    if "h " in match.group(1):
        time = match.group(1)
        h = time.split("h ")[0]
        m = time.split("h ")[1]
    else:
        h = 0
        m = match.group(1)
    next_rolls = datetime.datetime.now() + datetime.timedelta(hours=int(h), minutes=int(m))
    next_rolls = str(next_rolls.month)+ "_" + str(next_rolls.day) + "_" + str(next_rolls.hour) + "_"+ str(next_rolls.minute)

    print(f"Next rolls = {next_rolls}")
    
    #Can RT/Next RT
    match = re.search(r"\$rt.*?(available|\d+(?:h\ \d+)?)", tu_content)
    if match:
        if match.group(1) == "available":
            can_rt = True
        else:
            if "h " in match.group(1):
                time = match.group(1)
                h = time.split("h ")[0]
                m = time.split("h ")[1]
            else:
                h = 0
                m = match.group(1)
            next_rt = datetime.datetime.now() + datetime.timedelta(hours=int(h), minutes=int(m))
            can_rt = str(next_rt.month)+ "_" + str(next_rt.day) + "_" + str(next_rt.hour) + "_"+ str(next_rt.minute)
    elif not match:
        can_rt = False

    print(f"RT = {can_rt}")
    
    #Kakera Power
    match = re.search(r"Power:.*?(\d+)", tu_content)
    kp = int(match.group(1))

    print(f"Kakera power = {kp}")

    #Can DK
    match = re.search(r"\$dk.*?(ready|\d+(?:h\ \d+)?)", tu_content)
    if match.group(1) == "ready":
        can_dk = True
    else:
        can_dk = False

    print(f"Can $dk = {can_dk}")

    #Can Daily
    match = re.search(r"\$daily.*?available", tu_content)
    if match:
        can_daily = True
    else:
        can_daily = False

    print(f"Can $daily = {can_daily}")

    print("Tu parsed")

    return roll_amount, can_claim, next_claim, can_rt, kp, can_dk, can_daily, next_rolls

keep_alive()
try:
    client.run(token)
except:
    os.system("kill 1")