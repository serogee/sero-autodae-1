from discord.ext import commands
import asyncio


class Sniper(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global mudae
        mudae = self.client.get_user(432610292342587392)
        cuser = self.client.user
        cwait = self.client.wait_for
        cmentioned = cuser.mentioned_in
        asyncio_ensure = asyncio.ensure_future
        
        async def wish_claimer(message):
    
            mchannel = message.channel
            
            def dont_snipe(message1, message2):
                return message1 == message
        
            def dont_friendly_fire(message):
                return message.author == cuser and message.channel == mchannel
                
            edited, friendly = await asyncio.gather(
                    cwait("message_edit", timeout=5.3, check=dont_snipe),
                    cwait("message", timeout=5.3, check=dont_friendly_fire),
                    return_exceptions = True
                )
                
            if isinstance(edited, asyncio.TimeoutError) and isinstance(edited, asyncio.TimeoutError):

                        await message.components[0].children[0].click()
                        
                        try:
                            await cwait("message_edit", timeout=2, check=lambda x, y: message == x)
                            print("Claimed wish successfully")
                        except asyncio.TimeoutError:
                
                            #retries $rt if cooldown message or rt confirmation is received
                            while True:
                    
                                def check_rt_fail(cd_message):
                                    return "cooldown" in cd_message and cd_message.author == mudae and cd_message.channel == mchannel
                                
                                rtmessage = await mchannel.send("$rt")
                    
                                confirm, fail = await asyncio.gather(
                                    cwait("reaction_add", timeout=1, check=lambda rtreaction, user: rtreaction.message == rtmessage and user == mudae),
                                    cwait("message", timeout=1, check=check_rt_fail),
                                    return_exceptions=True
                                )
                                
                                if not isinstance(confirm, asyncio.TimeoutError) and isinstance (fail, asyncio.TimeoutError):
                                    print("RTed! Attempting claim...")
                
                                if isinstance(confirm, asyncio.TimeoutError) and not isinstance(fail, asyncio.TimeoutError):
                                    print("Can't RT")
                                
                                elif isinstance(confirm, asyncio.TimeoutError) and isinstance(fail, asyncio.TimeoutError):
                                    continue

                                break

                            await message.components[0].children[0].click()
                            

        while True:
                    
            #Check for wish
            def check_wish(message):
                return "Wished by" in message.content and cmentioned(message) and message.author == mudae
        
            #Wait for wish
            wish_spawn = await cwait("message", check=check_wish)
         
            asyncio_ensure(wish_claimer(wish_spawn))


                    
                    
            
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        rmessage = reaction.message
        rmreact = rmessage.add_reaction
        remoji = str(reaction.emoji)
        rmchannel = rmessage.channel
        rmcsend = rmchannel.send
        cuser = self.client.user
        cwait = self.client.wait_for
        cmentioned = cuser.mentioned_in
    
        def dont_snipe(message1, message2):
            return message1 == rmessage
    
        def dont_friendly_fire(message):
            return message.author == cuser and message.channel == rmessage.channel
    
        #Old wish claimer for other people's rolls, still works so I just copypasted
        #Needs update
        if "Wished by" in reaction.message.content and cmentioned(reaction.message):
            if user == reaction.message.author:
                edited, friendly = await asyncio.gather(
                    cwait("message_edit", timeout=5.3, check=dont_snipe),
                    cwait("message", timeout=5.3, check=dont_friendly_fire),
                    return_exceptions = True
                )
                if isinstance(edited, asyncio.TimeoutError) and isinstance(edited, asyncio.TimeoutError):
                
                    await rmreact(remoji)
                    
                    def check_success(message1, message2):
                        return message1 == rmessage
            
                    try:
                        await cwait("message_edit", timeout=2, check=check_success)
                        print("Claimed wish successfully")
                    except asyncio.TimeoutError:
                        await rmessage.remove_reaction(remoji, cuser)
            
                        #retries $rt if cooldown message or rt confirmation is received
                        while True:
                
                            def check_rt_fail(cd_message):
                                return "cooldown" in cd_message and cd_message.author == mudae and cd_message.channel == reaction.channel
                            
                            rtmessage = await rmcsend("$rt")
                
                            confirm, fail = await asyncio.gather(
                                cwait("reaction_add", timeout=1, check=lambda rtreaction, user: rtreaction.message == rtmessage and user == mudae),
                                cwait("message", timeout=1, check=check_rt_fail),
                                return_exceptions=True
                            )
            
                            if isinstance(confirm, asyncio.TimeoutError) and not isinstance(fail, asyncio.TimeoutError):
                                print("Can't RT")
                            
                            if not isinstance(confirm, asyncio.TimeoutError) and isinstance (fail, asyncio.TimeoutError):
                                print("RTed! Claiming wish...")
            
                            if isinstance(confirm, asyncio.TimeoutError) and not isinstance(fail, asyncio.TimeoutError):
                                print("Can't RT")
                            
                            if isinstance(confirm, asyncio.TimeoutError) and isinstance(fail, asyncio.TimeoutError):
                                continue

                            break

                        await rmreact(remoji)

        
    

def setup(client):
    client.add_cog(Sniper(client))