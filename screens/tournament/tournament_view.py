# screens/tournament_view.py
from screens.base_screen import BaseScreen
from commands import NoopCmd, ExitCmd


class TournamentView(BaseScreen):
    """Screen for viewing and managing a specific tournament."""
    def __init__(self, tournament, clubs, tournament_manager, club_manager):
        """Initialize the view."""
        self.tournament_manager = tournament_manager
        self.club_manager = club_manager
        self.clubs = clubs
        self.tournament = tournament

    def display_tournament(self):
        """Show tournament details and menu options."""
        print(f"\n🏆 TOURNAMENT: {self.tournament.name}")
        print(f"📍 Venue: {self.tournament.venue}")
        print(f"📅 Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"🔁 Rounds: {self.tournament.current_round}/{self.tournament.number_of_rounds}")
        # print("Test: " + str(self.tournament.rounds))
        print("\n👥 Players:")

        for player in self.tournament.players:
            print(f" - {player.name} ({player.chess_id})")

        print("\nOptions:")
        print("1. Register a player")
        print("2. Enter results for current match")
        print("3. Advance to next round")
        print("4. Generate tournament report")
        print("5. Create a new tournament")
        print("6. To view clubs list")
        print("7. To go back to main menu")

    def display(self):
        """Display the tournament view."""
        self.display_tournament()

    def generate_tournament_report(self):
        """Print a tournament summary report."""
        print("-Begin Report-")
        print(f"\n🏆 TOURNAMENT: {self.tournament.name}")
        print(f"📅 Dates: {self.tournament.start_date} to {self.tournament.end_date}")

        print("\n👥 Players (by points):")
        for i, p in enumerate(self.tournament.get_sorted_players_by_points(), 1):
            # points could be 0.5 increments
            pts = int(p.points) if p.points.is_integer() else p.points
            print(f"  {i}. {p.name} — {pts} pts")

        print("\n🧭 Rounds & Matches:")
        for i, rnd in enumerate(self.tournament.rounds, 1):
            print(f"  Round {i} of {self.tournament.number_of_rounds}")
            for m in rnd.matches:
                if getattr(m, "completed", False):
                    wtxt = "Tie" if getattr(m, "winner", None) is None else m.winner.name
                else:
                    wtxt = "—"
                print(f"    - {m.player1.name} vs {m.player2.name} | Completed: {m.completed} | Winner: {wtxt}")

        print("\n-End Report-")

    def get_command(self):
        """Prompt for user action and return the corresponding command."""
        while True:
            value = self.input_string("Choose an option")
            if value == "1":
                return NoopCmd("register-player",
                               tournament=self.tournament,
                               clubs=self.clubs,
                               club_manager=self.club_manager,
                               tournament_manager=self.tournament_manager)
            elif value == "2":
                return NoopCmd("enter-results", tournament=self.tournament, clubs=self.clubs)
            elif value == "3":
                print("Generating new round....")
                self.tournament.generate_next_round()
                self.display_tournament()
                print("New round generated!")
                # return NoopCmd("next-round", tournament=self.tournament)
            elif value == "4":
                self.generate_tournament_report()
                # return NoopCmd("generate-report", tournament=self.tournament)
            elif value == "5":
                return NoopCmd("create-tournament",
                               club_manager=self.club_manager,
                               tournament_manager=self.tournament_manager)
            elif value == "6":
                return NoopCmd("main-menu",
                               club_manager=self.club_manager,
                               tournament_manager=self.tournament_manager,
                               view_club=True)
            elif value == "7":
                return NoopCmd("main-menu",
                               club_manager=self.club_manager,
                               tournament_manager=self.tournament_manager)
            elif value.upper() == "X":
                print("X. Exit the program")
                return ExitCmd()
