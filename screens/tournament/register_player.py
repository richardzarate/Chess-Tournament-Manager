from screens.base_screen import BaseScreen
from commands import NoopCmd


class RegisterPlayer(BaseScreen):
    """Screen for registering players into a tournament."""
    def __init__(self, tournament, clubs, club_manager, tournament_manager):
        """Initialize the screen and list available players."""
        self.tournament = tournament
        self.clubs = clubs
        self.cm = club_manager
        self.tm = tournament_manager
        self.available_players = []
        for c in clubs:
            for p in c.players:
                if p not in self.tournament.players:
                    self.available_players.append(p)

    def display(self):
        """Show available players."""
        self.display_available_players(self.available_players)

    def display_available_players(self, players):
        """List given players with index numbers."""
        print("\n👥 Available Players for Registration:")
        if not players:
            print("No available players in this club.")
            return
        for i, player in enumerate(players, 1):
            print(f"{i}. {player.name}: {player.chess_id}")

        print()

    def choose_player(self, player_list):
        """Prompt to select a player from the list."""
        while True:
            self.display_available_players(player_list)
            print("Press q to return to previous menu")
            choice = input("Input: ")
            if choice.lower() == "q":
                return
            else:
                try:
                    index = int(choice)
                    if index < 1 or index > len(player_list):
                        print("Invalid input. Please choose a valid input")
                    else:
                        return player_list[index - 1]
                except ValueError:
                    print("❌ Please enter a valid number or 'q'.")

    def register_player(self, player):
        """Add a player to the tournament and remove from available list."""
        self.tournament.players.append(player)
        self.available_players.remove(player)
        print(f"✅ {player.name} has been registered.")
        input("[Enter] to continue...")

    def search_by_chessID(self):
        """Find and register a player by Chess ID."""
        if not self.available_players:
            print("No available players to search.")
            input("[Enter] to return...")
            return
        chess_id = self.input_string("Enter Chess ID").strip().lower()
        chess_id_matches = [p for p in self.available_players if p.chess_id.lower() == chess_id]

        if not chess_id_matches:
            print("❌ No player found with that Chess ID.")
            input("[Enter] to return")
            return
        else:
            print("ChessID matched....")
            player = self.choose_player(chess_id_matches)
            if player:
                self.register_player(player)

    def search_by_name(self):
        """Find and register a player by name keyword."""
        if not self.available_players:
            print("No available players to search.")
            input("[Enter] to return...")
            return

        keyword = self.input_string("Enter player name keyword").strip().lower()
        name_matches = [p for p in self.available_players if keyword in p.name.lower()]

        if not name_matches:
            print("❌ No players matched that name.")
            input("[Enter] to return...")
            return

        print("Name matches found...")
        player = self.choose_player(name_matches)
        if player:
            self.tournament.players.append(player)
            self.available_players.remove(player)
            print(f"✅ {player.name} has been registered.")
            input("[Enter] to continue...")

    def get_command(self):
        """Prompt for registration actions and return the next command."""
        while True:
            print("[1] Add a player")
            print("[2] Search by ChessID")
            print("[3] Search by player name")
            print("[0] To return to previous screen")

            choice = self.input_string("Input: ")
            if choice == "0":
                return NoopCmd("tournament-view",
                               tournament=self.tournament,
                               clubs=self.clubs,
                               club_manager=self.cm,
                               tournament_manager=self.tm)
            elif choice == "1":
                player = self.choose_player(self.available_players)
                if player:
                    self.register_player(player)
            elif choice == "2":
                self.search_by_chessID()
            elif choice == "3":
                self.search_by_name()

            else:
                print("❌ Invalid input. Please try again.\n")
