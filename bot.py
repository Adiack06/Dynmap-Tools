import discord
import json
import requests
from discord.ext import tasks
players = {}   


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def save_players():
    if not players:
        print("No players to save.")
        return

    with open("players.json", "w") as f:
        json.dump(players, f)
    print("Players saved.")

@tasks.loop(seconds = 10) # repeat after every 1 seconds
async def tracker():
    print("ting init")
    url = "http://shenanigans-group.com:8090/up/world/ShenanigansEM_S8v2/1675170588753"
    response = requests.get(url)
    user = client.get_user(<insert id>)
    data = response.json()   
    if response.status_code == 200:
        
        players = data["players"]
        for player in players:
            if -15494 <= player["x"] <= -13222 and 4672 <= player["z"] <= 7423 and player['name'] != "adiack":
                await user.send(f"Player name: {player['name']}")
                await user.send(f"Player location: {player['x']}, {player['y']},{player['z']}")
    else:
        await user.send(f"Failed to retrieve player data.")
        print("Failed to retrieve player data.")


#def search_by_attribute(array, attr, value):
    #for person in array:
        #if getattr(person, attr) == value:
            #return person

@client.event
async def on_ready():
    tracker.start()
    with open("players.json", "r") as f:
        players = json.load(f)
        print("players loaded")
        
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!rename"):
        new_name = message.content.split(" ")[1]
        players[message.author.id] = new_name
        save_players()
        await message.channel.send(f"{message.author.mention}'s minecraft name has been changed to {new_name}")

    if message.content.startswith("!info"):
        if str(message.author.id) in players:
            mc_name = players[str(message.author.id)]
            await message.channel.send(f"{message.author.mention} your minecraft name is {mc_name}")
        else:
            await message.channel.send(f"{message.author.mention} No information found")
    if message.content.startswith("!who"):
        url = "http://shenanigans-group.com:8090/up/world/ShenanigansEM_S8v2/1675170588753"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            players = data["players"]
            for player in players:
                if -15494 <= player["x"] <= -13222 and 4672 <= player["z"] <= 7423:
                    await message.channel.send(f"Player name: {player['name']}")
                    await message.channel.send(f"Player location: {player['x']}, {player['y']},{player['z']}")
        else:
            await message.channel.send(f"Failed to retrieve player data.")
            print("Failed to retrieve player data.")

client.run("<inset token>")

