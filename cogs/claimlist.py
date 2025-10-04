from discord.ext import commands #upm package(discord.py-self)
import json


def likesplit(text):
    text = text.replace("\n", " ")
    text_split = text.split("$")
    item_list = []
    for item in text_split:
        item = item.strip("\n\u200b ")
        item_list.append(item)
    return item_list

class Claimlist(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        mcontent = message.content
        mstart = mcontent.startswith
        mreact = message.add_reaction
        mchannel = message.channel
        mcid = mchannel.id

        if message.author.id != 396860451713187843:
            return

        #Global Likelist
        #Will be prioritized when no listed wish is found
        while True:
            try:
                #Global chara like
                if mstart(",lg "):
                    text = mcontent.replace(",lg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["LikelistGlobal"]["Characters"]
                    jcontent["LikelistGlobal"]["Characters"] = list(set(chars + ll))
                    print("Updated Global Character Likelist")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")

                #Global seies like
                if mstart(",lsg "):
                    text = mcontent.replace(",lsg ", "", 1)
                    series = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["LikelistGlobal"]["Series"]
                    jcontent["LikelistGlobal"]["Series"] = list(set(series + ll))
                    print("Updated Global Series Likelist")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
                #Global chara like remove
                if mstart(",lrg "):
                    text = mcontent.replace(",lrg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["LikelistGlobal"]["Characters"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["LikelistGlobal"]["Characters"] = ll
                    print("Updated Global Character Likelist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")

                #Global chara like remove all
                if mstart(",lrallg"):
                    text = mcontent.replace(",lrallg", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["LikelistGlobal"]["Characters"] = []
                    print("Cleaned Global Character Likelist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")

                #Global series like remove
                if mstart(",lsrg "):
                    text = mcontent.replace(",lsrg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["LikelistGlobal"]["Series"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["LikelistGlobal"]["Series"] = ll
                    print("Updated Global Series Likelist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")

                #Global series like remove all
                if mstart(",lsrallg"):
                    text = mcontent.replace(",lsrallg", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["LikelistGlobal"]["Series"] = []
                    print("Cleaned Global Series Likelist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
            except KeyError:
                with open("cogs/List.json", "r") as f:
                    jcontent = json.load(f)
                    
                jcontent["LikelistGlobal"] = {
                    "Characters": [],
                    "Series": []
                }
                
                with open("cogs/List.json", "w") as f:
                    json.dump(jcontent, f, indent=4)
                continue
            break

        #Global Wishlist
        #*same as last, but with Wishlist instead of Likelist
        #Will be claimed immedietly
        while True:
            try:
                if mstart(",wg "):
                    text = mcontent.replace(",wg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["WishlistGlobal"]["Characters"]
                    jcontent["WishlistGlobal"]["Characters"] = list(set(chars + ll))
                    print("Updated Global Character Wishlist")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
                if mstart(",wsg "):
                    text = mcontent.replace(",wsg ", "", 1)
                    series = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["WishlistGlobal"]["Series"]
                    jcontent["WishlistGlobal"]["Series"] = list(set(series + ll))
                    print("Updated Global Series Wishlis")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
        
                if mstart(",wrg "):
                    text = mcontent.replace(",wrg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["WishlistGlobal"]["Characters"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["WishlistGlobal"]["Characters"] = ll
                    print("Updated Global Character Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                    
                if mstart(",wrallg"):
                    text = mcontent.replace(",wrallg", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["WishlistGlobal"]["Characters"] = []
                    print("Cleaned Global Character Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                            
                if mstart(",wsrg "):
                    text = mcontent.replace(",wsrg ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["WishlistGlobal"]["Series"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["WishlistGlobal"]["Series"] = ll
                    print("Updated Global Series Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                                            
                if mstart(",wsrallg"):
                    text = mcontent.replace(",wsrallg", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["WishlistGlobal"]["Series"] = []
                    print("Cleaned Global Series Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
            except KeyError:
                with open("cogs/List.json", "r") as f:
                    jcontent = json.load(f)
                    
                jcontent["WishlistGlobal"] = {
                    "Characters": [],
                    "Series": []
                }
                
                with open("cogs/List.json", "w") as f:
                    json.dump(jcontent, f, indent=4)
                continue
            break
            
        #ChannelWishlist
        #*Same as last but specific to one channel
        #Will be claimed immedietly
        while True:
            try:
                if mstart(",w "):
                    text = mcontent.replace(",w ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent[f"Wishlist{mcid}"]["Characters"]
                    jcontent[f"Wishlist{mcid}"]["Characters"] = list(set(chars + ll))
                    print(f"Upadated {mchannel.name} Character Wishlist")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
                if mstart(",ws "):
                    text = mcontent.replace(",ws ", "", 1)
                    series = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent[f"Wishlist{mcid}"]["Series"]
                    jcontent[f"Wishlist{mcid}"]["Series"] = list(set(series + ll))
                    print(f"Upadated {mchannel.name} Series Wishlis")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
        
                if mstart(",wr "):
                    text = mcontent.replace(",wr ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent[f"Wishlist{mcid}"]["Characters"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent[f"Wishlist{mcid}"]["Characters"] = ll
                    print(f"Upadated {mchannel.name} Character Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                    
                if mstart(",wrall"):
                    text = mcontent.replace(",wrall", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent[f"Wishlist{mcid}"]["Characters"] = []
                    print(f"Cleaned {mchannel.name} Character Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                            
                if mstart(",wsr "):
                    text = mcontent.replace(",wsr ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent[f"Wishlist{mcid}"]["Series"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent[f"Wishlist{mcid}"]["Series"] = ll
                    print(f"Upadated {mchannel.name} Series Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                                            
                if mstart(",wsrall"):
                    text = mcontent.replace(",wsrall", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent[f"Wishlist{mcid}"]["Series"] = []
                    print(f"Cleaned {mchannel.name} Series Wishlist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
            except KeyError:
                with open("cogs/List.json", "r") as f:
                    jcontent = json.load(f)
                    
                jcontent[f"Wishlist{mcid}"] = {
                    "Characters": [],
                    "Series": []
                }
                
                with open("cogs/List.json", "w") as f:
                    json.dump(jcontent, f, indent=4)
                continue
            break

        #Blacklisting
        while True:
            try:
                if mstart(",b "):
                    text = mcontent.replace(",b ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["BlacklistGlobal"]["Characters"]
                    jcontent["BlacklistGlobal"]["Characters"] = list(set(chars + ll))
                    print("Updated Global Character Blacklist")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
                if mstart(",bs "):
                    text = mcontent.replace(",bs ", "", 1)
                    series = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                        
                    ll = jcontent["BlacklistGlobal"]["Series"]
                    jcontent["BlacklistGlobal"]["Series"] = list(set(series + ll))
                    print("Updated Global Series Wishlis")
        
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
        
                if mstart(",br "):
                    text = mcontent.replace(",br ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["BlacklistGlobal"]["Characters"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["BlacklistGlobal"]["Characters"] = ll
                    print("Updated Global Character Blacklist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                    
                if mstart(",brall"):
                    text = mcontent.replace(",brall", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["BlacklistGlobal"]["Characters"] = []
                    print("Cleaned Global Character Blacklist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                            
                if mstart(",bsr "):
                    text = mcontent.replace(",bsr ", "", 1)
                    chars = likesplit(text)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
        
                    ll = jcontent["BlacklistGlobal"]["Series"]
                    for char in list(set(chars) & set(ll)):
                        ll.remove(char)
                    jcontent["BlacklistGlobal"]["Series"] = ll
                    print("Updated Global Series Blacklist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                                            
                if mstart(",bsrall"):
                    text = mcontent.replace(",bsrall", "", 1)
                    
                    with open("cogs/List.json", "r") as f:
                        jcontent = json.load(f)
                    jcontent["BlacklistGlobal"]["Series"] = []
                    print("Cleaned Global Series Blacklist")
                    
                    with open("cogs/List.json", "w") as f:
                        json.dump(jcontent, f, indent=4)
                    await mreact("✅")
                        
            except KeyError:
                with open("cogs/List.json", "r") as f:
                    jcontent = json.load(f)
                    
                jcontent["BlacklistGlobal"] = {
                    "Characters": [],
                    "Series": []
                }
                
                with open("cogs/List.json", "w") as f:
                    json.dump(jcontent, f, indent=4)
                continue
            break

def setup(client):
    client.add_cog(Claimlist(client))