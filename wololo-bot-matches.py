import time
import discord
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

TOKEN = 'MTE0NjExMDE2MDcyNTYyMjg0NQ.Gz4VjC.-VMX53nHhI6deUQl5QjpT5vtQ-dn4bDn-bVRG4'
CHANNEL_ID = 1185690467501887598
# CHANNEL_ID = 974341698643689534

intents = discord.Intents.default()
intents.message_content = True

list_players = []


class PlayerWatched:
    def __init__(self, profile_id, discord_id, discord_name, last_rm_elo, new_rm_elo, last_tg_elo, new_tg_elo, steam_id):
        self.profile_id = profile_id
        self.discord_id = discord_id
        self.discord_name = discord_name

        self.url_companion = "https://www.aoe2companion.com/profile/" + str(profile_id)


class Player:
    def __init__(self, profile_id, player_name, new_elo, elo_change, result, color, team, civ):
        self.profile_id = profile_id
        self.player_name = player_name
        self.new_elo = new_elo
        if "↑" in elo_change:
            factor = "+"
        else:
            factor = "-"
        elo_change = str(elo_change.replace("\u2009", ""))
        elo_change = str(elo_change.replace(" ", ""))
        elo_change = str(elo_change.replace("↑", ""))
        elo_change = str(elo_change.replace("↓", ""))
        self.elo_change = factor + elo_change
        self.result = result
        self.color = color
        self.team = team
        if civ == "Armenians":
            self.civ = "Armenios"
        elif civ == "Aztecs":
            self.civ = "Aztecas"
        elif civ == "Bengalis":
            self.civ = "Bengalíes"
        elif civ == "Berbers":
            self.civ = "Bereberes"
        elif civ == "Bohemians":
            self.civ = "Bohemios"
        elif civ == "Britons":
            self.civ = "Britanos"
        elif civ == "Bulgarians":
            self.civ = "Búlgaros"
        elif civ == "Burgundians":
            self.civ = "Borgoñeses"
        elif civ == "Burmese":
            self.civ = "Birmanos"
        elif civ == "Byzantines":
            self.civ = "Bizantinos"
        elif civ == "Celts":
            self.civ = "Celtas"
        elif civ == "Chinese":
            self.civ = "Chinos"
        elif civ == "Cumans":
            self.civ = "Cumanos"
        elif civ == "Dravidians":
            self.civ = "Dravídicos"
        elif civ == "Ethiopians":
            self.civ = "Etíopes"
        elif civ == "Franks":
            self.civ = "Francos"
        elif civ == "Georgians":
            self.civ = "Georgianos"
        elif civ == "Goths":
            self.civ = "Godos"
        elif civ == "Gurjaras":
            self.civ = "Gurjaras"
        elif civ == "Hindustanis":
            self.civ = "Indostanos"
        elif civ == "Huns":
            self.civ = "Hunos"
        elif civ == "Incas":
            self.civ = "Incas"
        elif civ == "Italians":
            self.civ = "Italianos"
        elif civ == "Japanese":
            self.civ = "Japoneses"
        elif civ == "Khmer":
            self.civ = "Jemeres"
        elif civ == "Koreans":
            self.civ = "Coreanos"
        elif civ == "Lithuanians":
            self.civ = "Lituanos"
        elif civ == "Magyars":
            self.civ = "Magiares"
        elif civ == "Malay":
            self.civ = "Malayos"
        elif civ == "Malians":
            self.civ = "Malíes"
        elif civ == "Mayans":
            self.civ = "Mayas"
        elif civ == "Mongols":
            self.civ = "Mongoles"
        elif civ == "Persians":
            self.civ = "Persas"
        elif civ == "Poles":
            self.civ = "Polacos"
        elif civ == "Portuguese":
            self.civ = "Portugueses"
        elif civ == "Romans":
            self.civ = "Romanos"
        elif civ == "Saracens":
            self.civ = "Sarracenos"
        elif civ == "Sicilians":
            self.civ = "Sicilianos"
        elif civ == "Slavs":
            self.civ = "Eslavos"
        elif civ == "Spanish":
            self.civ = "Españoles"
        elif civ == "Tatars":
            self.civ = "Tártaros"
        elif civ == "Teutons":
            self.civ = "Teutones"
        elif civ == "Turks":
            self.civ = "Turcos"
        elif civ == "Vietnameses":
            self.civ = "Vietnamitas"
        elif civ == "Vikings":
            self.civ = "Vikingos"
        else:
            self.civ = civ


def get_color(style):
    # Azul
    if "rgba(64, 91, 255, 0.2)" in style:
        return "🔵"
    # Rojo
    elif "rgba(255, 0, 0, 0.2)" in style:
        return "🔴"
    # Verde
    elif "rgba(0, 255, 0, 0.2)" in style:
        return "🟢"
    # Amarillo
    elif "rgba(255, 255, 0, 0.2)" in style:
        return "🟡"
    # Cyan
    elif "rgba(0, 255, 255, 0.2)" in style:
        return "⚪"
    # Magenta
    elif "rgba(255, 87, 179, 0.2)" in style:
        return "🟣"
    # Naranja
    elif "rgba(255, 150, 0, 0.2)" in style:
        return "🟠"
    # Gris
    elif "rgba(121, 121, 121, 0.2)" in style:
        return "⚫"
    else:
        return ""


class Match:
    def __init__(self, match_id, mapname, completiontime, match_type, players, image_map):
        self.match_id = match_id
        self.mapname = mapname
        completiontime = completiontime.split("/")
        self.completiontime = completiontime[1] + "/" + completiontime[0] + "/" + completiontime[2]

        self.match_type = match_type
        self.players = players
        self.image_map = image_map


class MyClient(discord.Client):
    async def on_ready(self):
        print("Running")
        options = Options()
        service = Service()
        options.add_argument("-headless")

        driver = webdriver.Firefox(service=service, options=options)

        while True:
            print("New loop")
            matches_reported = []
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
                    steam_id = int(words[5])
                    new_rm_elo = None
                    new_tg_elo = None
                    player_watched = PlayerWatched(profile_id, discord_id, discord_name, last_elo, new_rm_elo,
                                                   last_tg_elo,
                                                   new_tg_elo, steam_id)
                    list_players.append(player_watched)

            with open(os.path.realpath(os.path.dirname(__file__)) + "/matches.txt") as f:
                lines = f.readlines()
                for line in lines:
                    matches_reported.append(line.replace("\n", ""))

            for p in list_players:
                try:
                    print()
                    print("Getting " + p.discord_name)
                    print(p.url_companion)
                    driver.get(p.url_companion)
                    time.sleep(7)
                    tbody = driver.find_element(By.TAG_NAME, "tbody")
                    matches_tr = tbody.find_elements(By.TAG_NAME, "tr")
                    for i in matches_tr:
                        match_id = \
                            i.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "div")[0].find_element(
                                By.TAG_NAME,
                                "div").find_elements(
                                By.TAG_NAME, "div")[0].text
                        print()
                        print(match_id)
                        if match_id not in matches_reported:
                            print("Not reported: " + match_id)

                            map_name = \
                                i.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "div")[0].find_element(
                                    By.TAG_NAME, "div").find_elements(By.TAG_NAME, "div")[1].text
                            match_type = \
                                i.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "div")[0].find_element(
                                    By.TAG_NAME, "div").find_elements(By.TAG_NAME, "div")[2].text
                            match_time = \
                                i.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "div")[0].find_element(
                                    By.TAG_NAME, "div").find_elements(By.TAG_NAME, "div")[3].get_attribute("title")
                            imagemap = i.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "div")[
                                0].find_element(
                                By.TAG_NAME, "img").get_attribute("src")

                            match = Match(match_id, map_name, match_time, match_type, [], imagemap)

                            players_team_1 = \
                            i.find_elements(By.TAG_NAME, "td")[1].find_elements(By.XPATH, "./*")[0].find_elements(
                                By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")
                            players_team_2 = \
                            i.find_elements(By.TAG_NAME, "td")[1].find_elements(By.XPATH, "./*")[0].find_elements(
                                By.XPATH, "./*")[1].find_elements(By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")

                            try:
                                for p1 in players_team_1:
                                    p1_stats = p1.text.split("\n")
                                    if "↓" in p1_stats[3]:
                                        result = "lose"
                                    else:
                                        result = "win"
                                    # Getting color
                                    style = p1.get_attribute("style")
                                    player_color = get_color(style)

                                    player1 = Player(0, p1_stats[1], p1_stats[2], p1_stats[3], result, player_color, 1,
                                                     p1_stats[0])
                                    match.players.append(player1)

                                for p2 in players_team_2:
                                    p2_stats = p2.text.split("\n")
                                    if "↓" in p2_stats[0]:
                                        result = "lose"
                                    else:
                                        result = "win"
                                    # Getting color
                                    style = p2.get_attribute("style")
                                    player_color = get_color(style)
                                    player2 = Player(0, p2_stats[2], p2_stats[1], p2_stats[0], result, player_color, 2,
                                                     p2_stats[3])
                                    match.players.append(player2)

                                print()
                                print("Notify")
                                print()
                                print(match.match_id)
                                print(match.match_type)
                                print(match.mapname)
                                print(match.image_map)
                                print(match.completiontime)
                                print()
                                message_rm = match.match_type + "\n\n"
                                message_rm = message_rm + match.completiontime
                                int_i = 0
                                team_1 = "```"
                                team_2 = "```"
                                for player in match.players:
                                    if int_i >= len(match.players) / 2:
                                        team_2 = team_2 + str(
                                            player.new_elo + " " + player.elo_change + " " + player.color + player.player_name + " (" + player.civ + ")")
                                        if player.result == "win":
                                            team_2 = team_2 + "🏆"
                                        else:
                                            team_2 = team_2 + "💀"
                                        team_2 = team_2 + "\n"
                                    else:
                                        team_1 = team_1 + str(
                                            player.new_elo + " " + player.elo_change + " " + player.color + player.player_name + " (" + player.civ + ")")
                                        if player.result == "win":
                                            team_1 = team_1 + "🏆"
                                        else:
                                            team_1 = team_1 + "💀"
                                        team_1 = team_1 + "\n"
                                    int_i = int_i + 1

                                team_1 = team_1 + "```"
                                team_2 = team_2 + "```"
                                message_footer = "https://www.aoe2insights.com/match/" + match.match_id + "/"
                                print("Sending message discord")
                                channel_to = await bot.fetch_channel(CHANNEL_ID)
                                embed_rm = discord.Embed(title=match.mapname, url=message_footer, description=message_rm, color=0x992d22)
                                embed_rm.set_thumbnail(
                                    url=match.image_map)
                                # embed_rm.set_footer(text=message_footer)
                                embed_rm.add_field(name="Equipo 1", value=team_1)
                                embed_rm.add_field(name="Equipo 2", value=team_2)
                                await channel_to.send(embed=embed_rm)
                                with open(os.path.realpath(os.path.dirname(__file__)) + "/matches.txt", 'a') as file:
                                    file.write(str(match.match_id) + "\n")
                                matches_reported.append(match.match_id)
                            except Exception as e:
                                print(e)

                            time.sleep(60)
                        else:
                            print("Already reported: " + match_id)
                            break
                except Exception as e:
                    print(e)


bot = MyClient(intents=intents)
bot.run(TOKEN)
