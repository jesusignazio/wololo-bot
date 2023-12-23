import datetime
import time
import discord
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

TOKEN = 'MTE0NjExMDE2MDcyNTYyMjg0NQ.Gz4VjC.-VMX53nHhI6deUQl5QjpT5vtQ-dn4bDn-bVRG4'
CHANNEL_ID = 1185690467501887598
# CHANNEL_ID = 974341698643689534

SPECTATE_ID = 1186267701996433458
# SPECTATE_ID = 974341698643689534

intents = discord.Intents.default()
intents.message_content = True

list_players = []


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)


class Match:
    def __init__(self, match_id, mapname, completiontime, match_type, players, image_map):
        self.match_id = match_id
        self.mapname = mapname

        self.match_type = match_type
        self.players = players
        self.image_map = image_map

        time_parse_format = "%d/%m/%Y, %I:%M %p"
        completiontime = completiontime.split("/")
        completiontime = completiontime[1] + "/" + completiontime[0] + "/" + completiontime[2]
        completiontime = datetime.datetime.strptime(completiontime, time_parse_format)
        time_parse_format_output = "%d/%m/%Y, %H:%M"
        self.completiontime = datetime.datetime.strftime(completiontime, time_parse_format_output)


class MatchWatchedHolder:
    def __init__(self, match_id, discord_message_id):
        self.match_id = match_id
        self.discord_message_id = discord_message_id


class PlayerWatched:
    def __init__(self, profile_id, discord_id, discord_name):
        self.profile_id = profile_id
        self.discord_id = discord_id
        self.discord_name = discord_name

        self.url_companion = "https://www.aoe2companion.com/profile/" + str(profile_id)


class Player:
    def __init__(self, profile_id, player_name, new_elo, elo_change, result, color, team, civ):
        self.profile_id = profile_id
        self.player_name = player_name
        self.new_elo = new_elo
        if elo_change == 0:
            self.elo_change = ""
        else:
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
        elif civ == "Vietnamese":
            self.civ = "Vietnamitas"
        elif civ == "Vikings":
            self.civ = "Vikingos"
        else:
            self.civ = civ

        def get_color_emoji():
            return "p" + str(self.color)


def get_color_old(style):
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


def get_color(style):
    # Azul
    if "rgba(64, 91, 255, 0.2)" in style:
        return 1
    # Rojo
    elif "rgba(255, 0, 0, 0.2)" in style:
        return 2
    # Verde
    elif "rgba(0, 255, 0, 0.2)" in style:
        return 3
    # Amarillo
    elif "rgba(255, 255, 0, 0.2)" in style:
        return 4
    # Cyan
    elif "rgba(0, 255, 255, 0.2)" in style:
        return 5
    # Magenta
    elif "rgba(255, 87, 179, 0.2)" in style:
        return 6
    # Naranja
    elif "rgba(255, 150, 0, 0.2)" in style:
        return 7
    # Gris
    elif "rgba(121, 121, 121, 0.2)" in style:
        return 8
    else:
        return 0


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
            matches_started = []
            with open(os.path.realpath(os.path.dirname(__file__)) + "/watched.txt") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    words = line.split("&&&")
                    profile_id = words[0]
                    discord_id = words[1]
                    discord_name = words[2]
                    player_watched = PlayerWatched(profile_id, discord_id, discord_name)
                    list_players.append(player_watched)

            with open(os.path.realpath(os.path.dirname(__file__)) + "/matches.txt") as f:
                lines = f.readlines()
                for line in lines:
                    matches_reported.append(line.replace("\n", ""))
            with open(os.path.realpath(os.path.dirname(__file__)) + "/matches-started.txt") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    words = line.split("&&&")
                    match_id = words[0]
                    discord_message_id = words[1]
                    match_watched = MatchWatchedHolder(match_id, discord_message_id)
                    matches_started.append(match_watched)

            for p in list_players:
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
                            p1_stats = players_team_1[0].text.split("\n")

                            if any(x.match_id == match_id for x in matches_started):
                                print("match already published as live")
                                FLAG_PUBLISHED_SPECTATE = True
                            else:
                                FLAG_PUBLISHED_SPECTATE = False

                            if len(p1_stats) < 4:
                                print("match currently playing")
                                FLAG_COMPLETED = False

                            else:
                                print("match completed")
                                FLAG_COMPLETED = True

                            # Flujo de toma de decisiones
                            print("Decision workflow")

                            if FLAG_COMPLETED:
                                for p1 in players_team_1:
                                    p1_stats = p1.text.split("\n")

                                    # Getting color
                                    style = p1.get_attribute("style")
                                    player_color = get_color(style)

                                    elo_change = p1_stats[3]
                                    if "↓" in p1_stats[3]:
                                        result = "lose"
                                    else:
                                        result = "win"

                                    player1 = Player(0, p1_stats[1], p1_stats[2], elo_change, result, player_color, 1,
                                                     p1_stats[0])
                                    match.players.append(player1)

                                for p2 in players_team_2:
                                    p2_stats = p2.text.split("\n")

                                    # Getting color
                                    style = p2.get_attribute("style")
                                    player_color = get_color(style)

                                    elo_change = p2_stats[0]
                                    if "↓" in p2_stats[0]:
                                        result = "lose"
                                    else:
                                        result = "win"
                                    player2 = Player(0, p2_stats[2], p2_stats[1], elo_change, result,
                                                     player_color, 1,
                                                     p2_stats[3])
                                    match.players.append(player2)

                            else:
                                for p1 in players_team_1:
                                    p1_stats = p1.text.split("\n")

                                    # Getting color
                                    style = p1.get_attribute("style")
                                    player_color = get_color(style)
                                    result = "none"
                                    elo_change = 0
                                    print(p1_stats)
                                    player1 = Player(0, p1_stats[1], p1_stats[2], elo_change, result, player_color,
                                                     1,
                                                     p1_stats[0])
                                    match.players.append(player1)

                                for p2 in players_team_2:
                                    p2_stats = p2.text.split("\n")

                                    # Getting color
                                    style = p2.get_attribute("style")
                                    player_color = get_color(style)
                                    result = "none"
                                    elo_change = 0
                                    player2 = Player(0, p2_stats[1], p2_stats[0], elo_change, result,
                                                     player_color,
                                                     1,
                                                     p2_stats[2])
                                    match.players.append(player2)

                            if not FLAG_COMPLETED and FLAG_PUBLISHED_SPECTATE:
                                print("Partida no completada y ya publicada para espectar")
                                break

                            if not FLAG_COMPLETED and not FLAG_PUBLISHED_SPECTATE:
                                print("Partida no completada y no publicada para espectar")
                                print()
                                print("Notify game started to spectate")
                                print()
                                print(match.match_id)
                                print(match.match_type)
                                print(match.mapname)
                                print(match.image_map)
                                print(match.completiontime)
                                print()

                                # get emojis
                                emoji_p1 = discord.utils.get(bot.emojis, name="p1")
                                emoji_p2 = discord.utils.get(bot.emojis, name="p2")
                                emoji_p3 = discord.utils.get(bot.emojis, name="p3")
                                emoji_p4 = discord.utils.get(bot.emojis, name="p4")
                                emoji_p5 = discord.utils.get(bot.emojis, name="p5")
                                emoji_p6 = discord.utils.get(bot.emojis, name="p6")
                                emoji_p7 = discord.utils.get(bot.emojis, name="p7")
                                emoji_p8 = discord.utils.get(bot.emojis, name="p8")

                                spectate_link = "https://aoe2lobby.com/w/" + match.match_id

                                message_rm = match.match_type + "\n"
                                message_rm = message_rm + match.completiontime

                                int_i = 0
                                team_1 = "```"
                                team_2 = "```"
                                for player in match.players:
                                    if player.color == 1:
                                        player_color_emoji = emoji_p1
                                    elif player.color == 2:
                                        player_color_emoji = emoji_p2
                                    elif player.color == 3:
                                        player_color_emoji = emoji_p3
                                    elif player.color == 4:
                                        player_color_emoji = emoji_p4
                                    elif player.color == 5:
                                        player_color_emoji = emoji_p5
                                    elif player.color == 6:
                                        player_color_emoji = emoji_p6
                                    elif player.color == 7:
                                        player_color_emoji = emoji_p7
                                    elif player.color == 8:
                                        player_color_emoji = emoji_p8
                                    else:
                                        player_color_emoji = emoji_p1
                                    if int_i >= len(match.players) / 2:
                                        team_2 = team_2 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
                                        team_2 = team_2 + "\n"
                                    else:
                                        team_1 = team_1 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
                                        team_1 = team_1 + "\n"
                                    int_i = int_i + 1

                                team_1 = team_1 + "```"
                                team_2 = team_2 + "```"
                                print("Sending message discord")
                                channel_to = await bot.fetch_channel(SPECTATE_ID)

                                view = Buttons()
                                view.add_item(
                                    discord.ui.Button(label="Ver como espectador",
                                                      style=discord.ButtonStyle.primary,
                                                      url=spectate_link))

                                embed_rm = discord.Embed(title=match.mapname, url=spectate_link,
                                                         description=message_rm, color=0x992d22)
                                embed_rm.set_thumbnail(
                                    url=match.image_map)
                                # embed_rm.set_footer(text=message_footer)
                                embed_rm.add_field(name="Equipo 1", value=team_1)
                                embed_rm.add_field(name="Equipo 2", value=team_2)
                                embed_sent = await channel_to.send(embed=embed_rm, view=view)
                                with open(os.path.realpath(os.path.dirname(__file__)) + "/matches-started.txt",
                                          'a') as file:
                                    file.write(str(match.match_id) + "&&&" + str(embed_sent.id) + "\n")
                                matched_started = MatchWatchedHolder(match.match_id, embed_sent.id)
                                matches_started.append(matched_started)

                            if FLAG_COMPLETED and not FLAG_PUBLISHED_SPECTATE:
                                print("Partida completada y no publicada para espectar, publicarla como completada")
                                print()
                                print("Notify game finished")
                                print()
                                print(match.match_id)
                                print(match.match_type)
                                print(match.mapname)
                                print(match.image_map)
                                print(match.completiontime)
                                print()

                                # get emojis
                                emoji_p1 = discord.utils.get(bot.emojis, name="p1")
                                emoji_p2 = discord.utils.get(bot.emojis, name="p2")
                                emoji_p3 = discord.utils.get(bot.emojis, name="p3")
                                emoji_p4 = discord.utils.get(bot.emojis, name="p4")
                                emoji_p5 = discord.utils.get(bot.emojis, name="p5")
                                emoji_p6 = discord.utils.get(bot.emojis, name="p6")
                                emoji_p7 = discord.utils.get(bot.emojis, name="p7")
                                emoji_p8 = discord.utils.get(bot.emojis, name="p8")

                                message_rm = match.match_type + "\n"
                                message_rm = message_rm + match.completiontime + "\n"
                                int_i = 0
                                team_1 = "```"
                                team_2 = "```"
                                for player in match.players:
                                    if player.color == 1:
                                        player_color_emoji = emoji_p1
                                    elif player.color == 2:
                                        player_color_emoji = emoji_p2
                                    elif player.color == 3:
                                        player_color_emoji = emoji_p3
                                    elif player.color == 4:
                                        player_color_emoji = emoji_p4
                                    elif player.color == 5:
                                        player_color_emoji = emoji_p5
                                    elif player.color == 6:
                                        player_color_emoji = emoji_p6
                                    elif player.color == 7:
                                        player_color_emoji = emoji_p7
                                    elif player.color == 8:
                                        player_color_emoji = emoji_p8
                                    else:
                                        player_color_emoji = emoji_p1
                                    if int_i >= len(match.players) / 2:
                                        team_2 = team_2 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
                                        if player.result == "win":
                                            team_2 = team_2 + "🏆"
                                        else:
                                            team_2 = team_2 + "💀"
                                        team_2 = team_2 + "\n"
                                    else:
                                        team_1 = team_1 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
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
                                embed_rm = discord.Embed(title=match.mapname, url=message_footer,
                                                         description=message_rm, color=0x992d22)
                                embed_rm.set_thumbnail(
                                    url=match.image_map)
                                # embed_rm.set_footer(text=message_footer)
                                embed_rm.add_field(name="Equipo 1", value=team_1)
                                embed_rm.add_field(name="Equipo 2", value=team_2)
                                await channel_to.send(embed=embed_rm)
                                with open(os.path.realpath(os.path.dirname(__file__)) + "/matches.txt",
                                          'a') as file:
                                    file.write(str(match.match_id) + "\n")
                                matches_reported.append(match.match_id)

                            if FLAG_COMPLETED and FLAG_PUBLISHED_SPECTATE:
                                print("Partida completada y publicada para espectar, borrarla de espectar y publicarla como completada")
                                # borrar match_started_holder de la lista y de matches-started.txt
                                for m in matches_started:
                                    if m.match_id == match_id:
                                        # borrar mensaje de discord
                                        channel_to = await bot.fetch_channel(SPECTATE_ID)
                                        try:
                                            msg = await channel_to.fetch_message(m.discord_message_id)
                                            await msg.delete()
                                        except Exception as e:
                                            print(e)
                                            print("Mensaje posiblemente ya borrado")
                                        matches_started.remove(m)
                                        with open(os.path.realpath(
                                                os.path.dirname(__file__)) + "/matches-started.txt",
                                                  'a') as file:
                                            for n in matches_started:
                                                file.write(
                                                    str(n.match_id) + "&&&" + str(n.discord_message_id) + "\n")
                                        break
                                # publicar partida
                                print()
                                print("Notify game finished")
                                print()
                                print(match.match_id)
                                print(match.match_type)
                                print(match.mapname)
                                print(match.image_map)
                                print(match.completiontime)
                                print()

                                # get emojis
                                emoji_p1 = discord.utils.get(bot.emojis, name="p1")
                                emoji_p2 = discord.utils.get(bot.emojis, name="p2")
                                emoji_p3 = discord.utils.get(bot.emojis, name="p3")
                                emoji_p4 = discord.utils.get(bot.emojis, name="p4")
                                emoji_p5 = discord.utils.get(bot.emojis, name="p5")
                                emoji_p6 = discord.utils.get(bot.emojis, name="p6")
                                emoji_p7 = discord.utils.get(bot.emojis, name="p7")
                                emoji_p8 = discord.utils.get(bot.emojis, name="p8")

                                message_rm = match.match_type + "\n"
                                message_rm = message_rm + match.completiontime + "\n"
                                int_i = 0
                                team_1 = "```"
                                team_2 = "```"
                                for player in match.players:
                                    if player.color == 1:
                                        player_color_emoji = emoji_p1
                                    elif player.color == 2:
                                        player_color_emoji = emoji_p2
                                    elif player.color == 3:
                                        player_color_emoji = emoji_p3
                                    elif player.color == 4:
                                        player_color_emoji = emoji_p4
                                    elif player.color == 5:
                                        player_color_emoji = emoji_p5
                                    elif player.color == 6:
                                        player_color_emoji = emoji_p6
                                    elif player.color == 7:
                                        player_color_emoji = emoji_p7
                                    elif player.color == 8:
                                        player_color_emoji = emoji_p8
                                    else:
                                        player_color_emoji = emoji_p1
                                    if int_i >= len(match.players) / 2:
                                        team_2 = team_2 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
                                        if player.result == "win":
                                            team_2 = team_2 + "🏆"
                                        else:
                                            team_2 = team_2 + "💀"
                                        team_2 = team_2 + "\n"
                                    else:
                                        team_1 = team_1 + str(
                                            player.new_elo + " " + player.elo_change + " " + str(player_color_emoji) + player.player_name + " (" + player.civ + ")")
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
                                embed_rm = discord.Embed(title=match.mapname, url=message_footer,
                                                         description=message_rm, color=0x992d22)
                                embed_rm.set_thumbnail(
                                    url=match.image_map)
                                # embed_rm.set_footer(text=message_footer)
                                embed_rm.add_field(name="Equipo 1", value=team_1)
                                embed_rm.add_field(name="Equipo 2", value=team_2)
                                await channel_to.send(embed=embed_rm)
                                with open(os.path.realpath(os.path.dirname(__file__)) + "/matches.txt",
                                          'a') as file:
                                    file.write(str(match.match_id) + "\n")
                                matches_reported.append(match.match_id)

                        except Exception as e:
                            print(e)
                            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                    else:
                        print("Already reported: " + match_id)
                        break

                time.sleep(10)


bot = MyClient(intents=intents)
bot.run(TOKEN)
