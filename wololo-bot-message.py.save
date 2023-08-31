import json
import time
import discord
import os
import requests

TOKEN = 'MTE0NjExMDE2MDcyNTYyMjg0NQ.Gz4VjC.-VMX53nHhI6deUQl5QjpT5vtQ-dn4bDn-bVRG4'
CHANNEL_ID = 799746255873376297

intents = discord.Intents.default()
intents.message_content = True

list_players = []

class PlayerWatched:
    def __init__(self, profile_id, discord_id, discord_name, elo):
        self.profile_id = profile_id
        self.discord_id = discord_id
        self.discord_name = discord_name
        self.elo = elo
        self.url = "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&profile_id=" + str(profile_id) + "&count=5"

class MyClient(discord.Client):

    async def on_ready(self):
        print("Running")
        #TODO open documents
        with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n", "")
                words = line.split("&&&")
                profile_id = words[0]
                discord_id = words[1]
                discord_name = words[2]
                elo = None
                player_watched = PlayerWatched(profile_id, discord_id, discord_name, elo)
                list_players.append(player_watched)

        message = "```"
        for p in list_players:
            #TODO get current elo
            try:
                print("Getting " + p.discord_name)
                resp = requests.get(url=p.url)
                data = resp.json()
                elo = data[0]['rating']
                p.elo = int(elo)

            except Exception as e:
                continue

            time.sleep(1)

        #Sort players by elo rating
        list_players.sort(key=lambda x: x.elo, reverse=True)

        i = 1
        for p in list_players:
            message = message + "{:02d}".format(i) + " " + str(p.elo) + " " + p.discord_name 
            if i == 1:
                message = message + "🥇"
            elif i == 2:
                message = message + "🥈"
            elif i == 3:
                message = message + "🥉"
            i += 1
            message = message + "\n"
        message = message + "```"

        print("Sending message")
        embed = discord.Embed(title="Ranking RM 1vs1", description=message, color=0x992d22)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049283724497404004/1049284070665900043/logotipo-dark-knight-knight-esport_100659-74_1.png")
        #embed.add_field(name="Test", value="Test")
        channel_to = await bot.fetch_channel(CHANNEL_ID)
        await channel_to.send(embed=embed)

        exit()

bot = MyClient(intents=intents)
bot.run(TOKEN)
