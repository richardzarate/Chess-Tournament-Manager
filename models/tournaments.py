from datetime import datetime
from .matches import Match
from .round import Round


class Tournaments:
    """Represents a chess tournament."""
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, name, venue, dates, number_of_rounds=0,
                 current_round=0, completed=False, players=None, rounds=None, **kwargs):
        """Initialize a tournament.

        Args:
            name (str): Tournament name.
            venue (str): Tournament venue.
            dates (dict): Dict with 'from' and 'to' dates (dd-mm-yyyy).
            number_of_rounds (int): Total rounds. Defaults to 0.
            current_round (int): Current round number. Defaults to 0.
            completed (bool): True if tournament finished.
            players (list): List of Player objects or chess IDs.
            rounds (list): List of Round objects.
        """
        self.name = name
        self.venue = venue
        # Validate date formats
        try:
            datetime.strptime(dates['from'], self.DATE_FORMAT)
            datetime.strptime(dates['to'], self.DATE_FORMAT)
        except (KeyError, ValueError):
            raise ValueError("Invalid date format in 'dates'. Expected format is dd-mm-yyyy.")

        self.dates = dates  # dictionary
        self.number_of_rounds = number_of_rounds  # int
        self.current_round = current_round  # int
        self.completed = completed  # bool
        self.players = players or []  # List of chess IDs
        self.rounds = rounds or []

    # === DATE HELPERS ===
    @property
    def start_date(self):
        """str: Start date in dd-mm-yyyy format."""
        return self.dates['from']

    @property
    def end_date(self):
        """str: End date in dd-mm-yyyy format."""
        return self.dates['to']

    def is_active_or_upcoming(self):
        """bool: True if the tournament is ongoing or has not ended."""
        today = datetime.today()
        end_date = datetime.strptime(self.dates['to'], self.DATE_FORMAT)
        return today <= end_date and self.current_round <= self.number_of_rounds

    def serialize(self):
        """dict: JSON-serializable tournament data."""
        return {
            "name": self.name,
            "venue": self.venue,
            "dates": self.dates,  # already {"from":..., "to":...}
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": [p.chess_id for p in self.players],  # <-- IDs
            "rounds": [r.serialize() for r in self.rounds]  # <-- list[list[match]]
        }

    def get_sorted_players_by_points(self):
        """list: Players sorted by points (desc) then name."""
        return sorted(self.players, key=lambda p: (-p.points, p.name))

    def generate_next_round(self):
        """Generate and add the next round, pairing players by current standings.

        Handles odd player count by giving a bye to the lowest-ranked player.
        Returns:
            Round: The newly created round, or None if max rounds reached.
        """
        # stop if we already reached the max number of rounds
        if self.current_round >= self.number_of_rounds:
            # no new round generated
            self.completed = True
            return None

        players = self.get_sorted_players_by_points()  # list[Player]
        matches = []

        # Handle bye if odd number of players: give the lowest-ranked a bye (common Swiss rule = 1 point)
        bye_player = None
        if len(players) % 2 == 1:
            bye_player = players.pop()  # lowest-ranked after sorting
            bye_player.points += 1  # bye = full point (adjust if your rules differ)

        # Pair adjacent players
        for i in range(0, len(players), 2):
            p1 = players[i]
            p2 = players[i + 1]
            matches.append(Match(player1=p1, player2=p2))

        new_round = Round(matches=matches)
        self.rounds.append(new_round)
        self.current_round = len(self.rounds)
        self.rounds.insert(0, new_round)
