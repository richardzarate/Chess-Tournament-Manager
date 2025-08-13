class Match:
    """
    JSON schema target:
    {
        "players": [ "<id1>", "<id2>" ],
        "completed": <bool>,
        "winner": "<id1>|<id2>|null"
    }
    """

    def __init__(self, player1, player2, completed=False, winner=None):
        """
        result: "player1" | "player2" | "tie" | None
        """
        self.player1 = player1
        self.player2 = player2
        self.completed = completed
        # if result is not None:
        #     self.set_result(result)
        self.winner = winner
    # --- scoring/result ---

    def set_result(self, winner_index):
        """
        Sets the match result based on an index:
          0 -> player1 wins (+1 point)
          1 -> player2 wins (+1 point)
          2 -> tie (+0.5 each)
        """
        # Prevent setting result twice
        if getattr(self, "completed", False):
            raise ValueError("Match result already set!")

        # Validate input
        if winner_index not in (0, 1, 2):
            raise ValueError("Invalid winner_index. Use 0 (p1), 1 (p2), or 2 (tie).")

        # Assign points and track winner
        if winner_index == 0:
            self.player1.points += 1
            self.winner = self.player1
        elif winner_index == 1:
            self.player2.points += 1
            self.winner = self.player2
        elif winner_index == 2:
            self.player1.points += 0.5
            self.player2.points += 0.5
            self.winner = None  # tie
        self.completed = True

    def serialize(self):
        return {
            "players": [self.player1.chess_id, self.player2.chess_id],
            "completed": bool(getattr(self, "completed", False)),
            "winner": None if getattr(self, "winner", None) is None else self.winner.chess_id
        }
