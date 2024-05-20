import time
import discord
import os
import requests

TOKEN = 'MTE0NjExMDE2MDcyNTYyMjg0NQ.GGHN-q.9NiS9Agtu3JxHKpRH-rUaQ6e_4VFP5ZhOiWBG0'
CHANNEL_ID = 799746255873376297

intents = discord.Intents.default()
intents.message_content = True

list_players = []


class PlayerWatched:
    def __init__(self, profile_id, discord_id, discord_name, last_rm_elo, new_rm_elo, last_tg_elo, new_tg_elo, last_ew_elo, new_ew_elo, steam_id):
        self.profile_id = profile_id
        self.discord_id = discord_id
        self.discord_name = discord_name

        self.last_rm_elo = last_rm_elo
        self.new_rm_elo = new_rm_elo
        self.max_rm_elo = 0
        self.last_tg_elo = last_tg_elo
        self.new_tg_elo = new_tg_elo
        self.max_tg_elo = 0
        self.last_ew_elo = last_ew_elo
        self.new_ew_elo = 0
        self.steam_id = steam_id

        self.url_relic = "https://aoe-api.reliclink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/" + str(steam_id) + "%22]"
        self.url_rm = "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&profile_id=" + str(profile_id) + "&count=1"
        self.url_tg = "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=4&profile_id=" + str(profile_id) + "&count=1"
        self.url_ew = "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=13&profile_id=" + str(profile_id) + "&count=1"

    def get_rm_elo_diff(self):
        if self.last_rm_elo == 0:
            return ""
        else:
            diff = self.new_rm_elo - self.last_rm_elo
            if diff < 0:
                return " (" + str(diff) + ") "
            elif diff > 0:
                return " (+" + str(diff) + ") "
            else:
                return ""

    def get_tg_elo_diff(self):
        if self.last_tg_elo == 0:
            return ""
        else:
            diff = self.new_tg_elo - self.last_tg_elo
            if diff < 0:
                return " (" + str(diff) + ") "
            elif diff > 0:
                return " (+" + str(diff) + ") "
            else:
                return ""

    def get_ew_elo_diff(self):
        if self.last_ew_elo == 0:
            return ""
        else:
            diff = self.new_ew_elo - self.last_ew_elo
            if diff < 0:
                return " (" + str(diff) + ") "
            elif diff > 0:
                return " (+" + str(diff) + ") "
            else:
                return ""


class MyClient(discord.Client):
    async def on_ready(self):
        print("Running")
        with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n", "")
                words = line.split("&&&")
                profile_id = words[0]
                discord_id = words[1]
                discord_name = words[2]
                last_elo = int(words[3])
                last_tg_elo = int(words[4])
                last_ew_elo = int(words[5])
                steam_id = int(words[6])
                new_rm_elo = None
                new_tg_elo = None
                new_ew_elo = None
                player_watched = PlayerWatched(profile_id, discord_id, discord_name, last_elo, new_rm_elo, last_tg_elo, new_tg_elo, last_ew_elo, new_ew_elo, steam_id)
                list_players.append(player_watched)

        for p in list_players:
            try:
                print("Getting " + p.discord_name)

                resp = requests.get(url=p.url_relic)
                data = resp.json()
                for i in range(0, len(data['leaderboardStats'])):
                    if int(data['leaderboardStats'][i]['leaderboard_id']) == 3:  # RM
                        new_rm_elo = int(data['leaderboardStats'][i]['rating'])
                        p.new_rm_elo = new_rm_elo
                    elif int(data['leaderboardStats'][i]['leaderboard_id']) == 4:  # TG
                        new_tg_elo = int(data['leaderboardStats'][i]['rating'])
                        p.new_tg_elo = new_tg_elo
                    elif int(data['leaderboardStats'][i]['leaderboard_id']) == 27:  # EW
                        new_ew_elo = 0
                        new_ew_elo = int(data['leaderboardStats'][i]['rating'])
                        print(new_ew_elo)
                        p.new_ew_elo = new_ew_elo

                # TODO get max ELO

            except Exception as e:
                print(e)
                p.new_rm_elo = p.last_rm_elo
                p.new_tg_elo = p.last_tg_elo
                p.new_ew_elo = p.last_ew_elo

            time.sleep(1)

        """Sort players by new RM elo rating"""
        list_players.sort(key=lambda x: x.new_rm_elo, reverse=True)

        i = 1
        message_rm = "```"
        for p in list_players:
            message_rm = message_rm + "{:02d}".format(i) + " " + str(p.new_rm_elo).zfill(4) + " " + p.discord_name + p.get_rm_elo_diff()
            if i == 1:
                message_rm = message_rm + "🥇"
            elif i == 2:
                message_rm = message_rm + "🥈"
            elif i == 3:
                message_rm = message_rm + "🥉"
            i += 1
            message_rm = message_rm + "\n"
        message_rm = message_rm + "```"

        """Sort players by new TG elo rating"""
        list_players.sort(key=lambda x: x.new_tg_elo, reverse=True)

        i = 1
        message_tg = "```"
        for p in list_players:
            message_tg = message_tg + "{:02d}".format(i) + " " + str(p.new_tg_elo).zfill(4) + " " + p.discord_name + p.get_tg_elo_diff()
            if i == 1:
                message_tg = message_tg + "🥇"
            elif i == 2:
                message_tg = message_tg + "🥈"
            elif i == 3:
                message_tg = message_tg + "🥉"
            i += 1
            message_tg = message_tg + "\n"
        message_tg = message_tg + "```"

        """Sort players by new EW elo rating"""
        list_players.sort(key=lambda x: x.new_ew_elo, reverse=True)

        i = 1
        message_ew = "```"
        for p in list_players:
            message_ew = message_ew + "{:02d}".format(i) + " " + str(p.new_ew_elo).zfill(
                4) + " " + p.discord_name + p.get_ew_elo_diff()
            if i == 1:
                message_ew = message_ew + "🥇"
            elif i == 2:
                message_ew = message_ew + "🥈"
            elif i == 3:
                message_ew = message_ew + "🥉"
            i += 1
            message_ew = message_ew + "\n"
        message_ew = message_ew + "```"

        channel_to = await bot.fetch_channel(CHANNEL_ID)

        print("Purge channel content")
        try:
            await channel_to.purge(limit=2)
        except Exception as e:
            print(e)

        print("Sending message RM")
        embed_rm = discord.Embed(title="Ranking RM 1vs1", description=message_rm, color=0x992d22)
        embed_rm.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049283724497404004/1049284070665900043/logotipo-dark-knight-knight-esport_100659-74_1.png")
        await channel_to.send(embed=embed_rm)

        print("Sending message TG")
        embed_tg = discord.Embed(title="Ranking TG", description=message_tg, color=0x1f8b4c)
        embed_tg.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049283724497404004/1049284070665900043/logotipo-dark-knight-knight-esport_100659-74_1.png")
        await channel_to.send(embed=embed_tg)

        print("Sending message EW")
        embed_tg = discord.Embed(title="Ranking EW", description=message_ew, color=0x0000CD)
        embed_tg.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1049283724497404004/1049284070665900043/logotipo-dark-knight-knight-esport_100659-74_1.png")
        await channel_to.send(embed=embed_tg)

        """Clear watched.txt file"""
        with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt", 'w') as f:
            pass

        """Save new content to watched.txt"""
        for p in list_players:
            with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt", 'a') as f:
                f.write(p.profile_id + "&&&" + p.discord_id + "&&&" + p.discord_name + "&&&" + str(p.new_rm_elo) + "&&&" + str(p.new_tg_elo) + "&&&" + str(p.new_ew_elo) + "&&&" + str(p.steam_id) + "\n")
        exit()


bot = MyClient(intents=intents)
bot.run(TOKEN)
