from datetime import datetime
from commands import NoopCmd
from screens.base_screen import BaseScreen


class CreateTournamentView(BaseScreen):
    """Screen for creating a new tournament."""
    def __init__(self, club_manager, tournament_manager):
        """Initialize the view.

        Args:
            club_manager: Manages chess clubs.
            tournament_manager: Manages tournaments.
        """
        self.cm = club_manager
        self.tm = tournament_manager

    def display(self):
        """Show creation prompt header."""
        print("Please enter information for the tournament being created:")

    def _get_valid_date(self, prompt="Enter date (dd-mm-yyyy): "):
        """Prompt for a valid date in dd-mm-yyyy format."""
        while True:
            date_str = input(prompt).strip()
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
                return date_str
            except ValueError:
                print("❌ Invalid date format. Please use dd-mm-yyyy.")

    def _get_positive_int(self, prompt):
        """Prompt for a positive integer."""
        while True:
            s = input(prompt).strip()
            try:
                n = int(s)
                if n <= 0:
                    raise ValueError
                return n
            except ValueError:
                print("❌ Please enter a positive whole number.")

    def get_command(self):
        """Collect tournament info and create it via the manager."""
        today = datetime.today().date()

        while True:
            name = input("Enter tournament name: ").strip()
            venue = input("Enter venue: ").strip()

            start_date_str = self._get_valid_date("Enter start date (dd-mm-yyyy): ")
            end_date_str = self._get_valid_date("Enter end date (dd-mm-yyyy): ")

            start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
            end_date = datetime.strptime(end_date_str,   "%d-%m-%Y").date()

            # validations
            if start_date < today:
                print("❌ Start date cannot be in the past. Please try again from the beginning.\n")
                continue

            if end_date < start_date:
                print("❌ End date must be on or after the start date. Please try again from the beginning.\n")
                continue

            number_of_rounds = self._get_positive_int("Enter number of rounds: ")

            dates = {"from": start_date_str, "to": end_date_str}
            self.tm.create(name=name, venue=venue, dates=dates, number_of_rounds=number_of_rounds)

            print(f"✅ Tournament '{name}' created at {venue} ({start_date_str} →"
                  f" {end_date_str}), {number_of_rounds} rounds.")
            print("To add more info, open the created tournament from the main menu.")
            print("Tournament created, now returning to main menu...")
            return NoopCmd("main-menu", club_manager=self.cm, tournament_manager=self.tm)
