from screens.base_screen import BaseScreen
from commands import NoopCmd


class RoundView(BaseScreen):
    """Screen for viewing matches in the current tournament round."""
    def __init__(self, tournament, clubs):
        """Initialize the round view."""
        self.tournament = tournament
        self.clubs = clubs

    def display(self):
        """Display all matches in the current round."""
        self.display_matches()

    def display_matches(self):
        """List matches with their completion status and winner."""
        cr = self.tournament.current_round
        nr = self.tournament.number_of_rounds
        rounds = self.tournament.rounds

        if not (1 <= cr <= len(rounds)):
            print(f"Round {cr} of {nr} (no data)")
            return

        print(f"Round {cr} of {nr}")
        for i, match in enumerate(rounds[cr - 1].matches, 1):
            if match.completed:
                if match.winner is None:
                    winner_txt = "Tie"
                else:
                    winner_txt = match.winner
            else:
                winner_txt = "—"

            print(f"{i}. {match.player1.name} vs {match.player2.name} "
                  f"- Completed: {match.completed} - Winner: {winner_txt}")

    def get_command(self):
        """Prompt for match result entry and return the next command."""
        first_loop = True
        while True:
            if not first_loop:
                self.display_matches()
            # self.display()
            print("_____________________________________________________________________________")
            print("Pick the number of the match you would like to enter results for")
            print('Enter "b" to go back to tournament screen')

            cr_idx = self.tournament.current_round - 1
            rounds = self.tournament.rounds
            if not (0 <= cr_idx < len(rounds)):
                print("No matches for the current round.")
                return NoopCmd("tournament-view", tournament=self.tournament)

            current_round_matches = rounds[cr_idx].matches

        # while True:
            try:
                choice = input("Input: ").strip()
                if choice.lower() == "b":
                    return NoopCmd("tournament-view", tournament=self.tournament, clubs=self.clubs)

                index = int(choice) - 1
                if 0 <= index < len(current_round_matches):
                    match = current_round_matches[index]

                    if getattr(match, "completed", False):
                        print("This match has already been completed! Please pick one that's not completed yet.")
                        first_loop = False
                        continue

                    print(f"1. {match.player1.name}: {match.player1.chess_id}")
                    print(f"2. {match.player2.name}: {match.player2.chess_id}")
                    print("3. Set the match as a tie")
                    print("4. To go back to previous options")

                    while True:
                        try:
                            result_choice = input("Please pick between 1, 2, 3, or 4: ").strip()
                            if result_choice == "4":
                                first_loop = False
                                break
                            if result_choice in ("1", "2", "3"):
                                match.set_result(int(result_choice) - 1)  # 0=p1, 1=p2, 2=tie
                                print("Result recorded.")
                                first_loop = False
                                break
                            else:
                                print("Invalid choice. Please pick 1, 2, 3, or 4.")
                        except ValueError:
                            print("Please enter a number (1, 2, 3, or 4).")
                else:
                    print("Invalid match number.")
            except ValueError:
                print("Please pick only given choices (valid match number or 'b').")
