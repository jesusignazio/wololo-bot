import datetime
import random
import time
import os
import sys
import pickle

list_players = []


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


class Player:
    def __init__(self, profile_id, discord_id, discord_name, elo_rm, elo_tg, steam_id):
        self.profile_id = profile_id
        self.discord_id = discord_id
        self.discord_name = discord_name
        self.elo_rm = elo_rm
        self.elo_tg = elo_tg
        self.steam_id = steam_id
    def __repr__(self):
        return f"PlayerWatched({self.profile_id}, {self.discord_id}, {self.discord_name})"


def load_players_from_text(file_path):
    players = []
    with open(file_path, 'r') as file:
        for line in file:
            profile_id, discord_id, discord_name, elo_rm, elo_tg, steam_id = line.strip().split('&&&')
            players.append(Player(profile_id, discord_id, discord_name, elo_rm, elo_tg, steam_id))
    return players


def save_players_to_pickle(players, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(players, file)


def load_ids_from_text(file_path):
    ids = []
    with open(file_path, 'r') as file:
        for line in file:
            id = line.strip()
            ids.append(id)
    return ids


def save_ids_to_pickle(ids, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(ids, file)


# Example usage:
text_file_path = 'matches-started.txt'  # Path to your text file containing IDs
pickle_file_path = 'matches-started.pkl'  # Path where you want to save the pickle file

# Load IDs from the text file
ids = load_ids_from_text(text_file_path)

# Save the IDs to a pickle file
save_ids_to_pickle(ids, pickle_file_path)

print("IDs have been successfully migrated to pickle format.")
