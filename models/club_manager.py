import json
from pathlib import Path

from .club import ChessClub


class ClubManager:
    def __init__(self, data_folder="data/clubs"):
        datadir = Path(data_folder)
        self.data_folder = datadir
        self.clubs = []
        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    self.clubs.append(ChessClub(filepath))
                except json.JSONDecodeError:
                    print(filepath, "is invalid JSON file.")

    def get_player_by_chess_id(self, chess_id):
        for club in self.clubs:
            for player in club.players:
                if player.chess_id == chess_id:
                    return player
        return None  # If not found

    def create(self, name):
        filepath = self.data_folder / (name.replace(" ", "") + ".json")
        club = ChessClub(name=name, filepath=filepath)
        club.save()

        self.clubs.append(club)
        return club
