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

        Avoids repeat pairings from previous rounds when possible by scanning ahead
        and swapping opponents. If no valid opponent exists (late-round corner case),
        a rematch is allowed as a last resort.

        Returns:
            Round | None: The newly created round, or None if max rounds reached.
        """
        # Stop if we already reached the maximum number of rounds
        if self.current_round >= self.number_of_rounds:
            self.completed = True
            return None

        sorted_players = self.get_sorted_players_by_points()
        new_matches = []

        # Build a lookup of all previous pairings as sets of two player IDs
        previous_pairings = set()
        for previous_round in self.rounds:
            for previous_match in previous_round.matches:
                player_a_id = getattr(previous_match.player1, "chess_id", previous_match.player1)
                player_b_id = getattr(previous_match.player2, "chess_id", previous_match.player2)
                previous_pairings.add(frozenset({player_a_id, player_b_id}))

        def have_played_before(player_a, player_b) -> bool:
            return frozenset({player_a.chess_id, player_b.chess_id}) in previous_pairings

        # Handle bye if odd number of players: give the lowest-ranked a bye (1 point)
        bye_player = None
        if len(sorted_players) % 2 == 1:
            bye_player = sorted_players.pop()  # lowest-ranked after sorting
            bye_player.points += 1

        # Pair players, avoiding repeats when possible
        current_index = 0
        while current_index < len(sorted_players):
            current_player = sorted_players[current_index]

            # Find the first opponent that current_player has not played yet
            opponent_index = current_index + 1
            valid_opponent_index = None
            while opponent_index < len(sorted_players):
                potential_opponent = sorted_players[opponent_index]
                if not have_played_before(current_player, potential_opponent):
                    valid_opponent_index = opponent_index
                    break
                opponent_index += 1

            if valid_opponent_index is None:
                # No valid opponent found, fallback to immediate next player
                opponent_player = sorted_players[current_index + 1]
            else:
                # Swap chosen opponent into the immediate next position
                if valid_opponent_index != current_index + 1:
                    sorted_players[current_index + 1], sorted_players[valid_opponent_index] = (
                        sorted_players[valid_opponent_index],
                        sorted_players[current_index + 1],
                    )
                opponent_player = sorted_players[current_index + 1]

            new_matches.append(Match(player1=current_player, player2=opponent_player))
            current_index += 2  # move to the next pair

        # Create and add the new round
        next_round = Round(matches=new_matches)
        self.rounds.append(next_round)
        self.current_round = len(self.rounds)
        return next_round
