import json
from pathlib import Path
from .tournaments import Tournaments
from .player import Player
from .matches import Match
from .round import Round  # or whatever the filename/class is


class TournamentManager:
    """Manages tournaments, including creation, loading, saving, and completion."""
    def __init__(self, club_manager, data_folder="data/tournaments"):
        """Initialize the manager.

        Args:
            club_manager: Club manager instance for player lookups.
            data_folder (str): Path to store tournament JSON files.
        """
        self.club_manager = club_manager
        self.data_folder = Path(data_folder)
        self.in_progress_file = self.data_folder / "in-progress.json"
        self.completed_file = self.data_folder / "completed.json"

        # In-memory lists
        self.in_progress = []
        self.completed = []

        self._load_tournaments()

    def _load_tournaments(self):
        """Load tournaments from JSON files into memory."""
        if self.in_progress_file.exists():
            with open(self.in_progress_file, "r") as f:
                data = json.load(f)
                self.in_progress = [self._load_single_tournament(t) for t in data]

        if self.completed_file.exists():
            with open(self.completed_file, "r") as f:
                data = json.load(f)
                self.completed = [self._load_single_tournament(t) for t in data]

    def _load_single_tournament(self, data):
        """Create a Tournaments object from JSON data."""
        tournament = Tournaments(**data)

        # Resolve players (with placeholders)
        tournament.players = [
            self.club_manager.get_player_by_chess_id(cid)
            or Player(name="Unaffiliated Player", email="N/A", chess_id=cid, birthday="01-01-1900")
            for cid in tournament.players
        ]
        id_map = {p.chess_id: p for p in tournament.players}

        rounds_obj = []
        for r in data["rounds"]:
            # accept both shapes: list-of-matches OR {"matches": [...]}
            match_items = r.get("matches") if isinstance(r, dict) else r
            if not isinstance(match_items, list):
                raise ValueError(f"Invalid round shape: {type(r)}")

            matches = []
            for mdata in match_items:
                id1, id2 = mdata["players"]
                p1 = id_map[id1]
                p2 = id_map[id2]
                win_player = id_map.get(mdata.get("winner")) if mdata.get("winner") else None

                m = Match(player1=p1, player2=p2)
                if mdata.get("completed", False):
                    if win_player is None:
                        m.set_result(2)  # tie
                    elif win_player is p1:
                        m.set_result(0)  # p1 wins
                    elif win_player is p2:
                        m.set_result(1)  # p2 wins
                    else:
                        m.set_result(2)  # fallback tie
                matches.append(m)

            rounds_obj.append(Round(matches=matches))

        tournament.rounds = rounds_obj
        return tournament

    def save(self):
        """Save all tournaments to JSON files."""
        with open(self.in_progress_file, "w") as f:
            json.dump([t.serialize() for t in self.in_progress], f, indent=4)

        with open(self.completed_file, "w") as f:
            json.dump([t.serialize() for t in self.completed], f, indent=4)

    def create(self, name, venue, dates, number_of_rounds):
        """Create a new tournament and save it."""
        tournament = Tournaments(
            name=name,
            venue=venue,
            dates=dates,
            rounds=[],
            number_of_rounds=number_of_rounds,
            current_round=1,
            players=[]
        )
        self.in_progress.append(tournament)
        self.save()
        return tournament

    def complete_tournament(self, tournament):
        """Mark a tournament as completed and save."""
        self.in_progress.remove(tournament)
        self.completed.append(tournament)
        self.save()
