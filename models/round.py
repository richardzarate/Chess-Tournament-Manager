class Round:
    """Represents a tournament round containing multiple matches.

    Args:
        matches (list): List of match objects. Defaults to empty list.

    Attributes:
        matches (list): Matches scheduled for this round.
    """
    def __init__(self, matches):
        """Initialize a round.

        Args:
            matches (list): List of match objects. Defaults to empty list.
        """
        self.matches = matches if matches else []

    def is_complete(self):
        """bool: True if all matches are marked completed."""
        return all(match.completed is not None for match in self.matches)

    def serialize(self):
        """dict: JSON-serializable representation of the round."""
        return {
            "matches": [match.serialize() for match in self.matches],
        }
