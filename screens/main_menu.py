from commands import ExitCmd, NoopCmd
from .base_screen import BaseScreen


class MainMenu(BaseScreen):
    """Main menu screen for navigating clubs and tournaments."""

    def __init__(self, club_manager, tournament_manager, **kwargs):
        """Initialize the menu.

        Args:
            club_manager: Manages chess clubs.
            tournament_manager: Manages tournaments.
            **kwargs: Optional parameters (view_club: bool to start in club view).
        """
        self.cm = club_manager
        self.tm = tournament_manager
        self.view_club = kwargs.get("view_club", False)

        # self.clubs = club_manager.clubs
        # self.in_progress_tournaments = tournament_manager.in_progress
        # self.completed_tournaments = tournament_manager.completed

    def display(self):
        """Display active tournaments or clubs."""
        if self.tm.in_progress and not self.view_club:

            self.display_active_or_upcoming_tournaments()
        else:
            print("There are no active tournaments, here are the current chess clubs available")
            self.display_clubs()

    def display_clubs(self):
        """List all clubs."""
        for idx, club in enumerate(self.cm.clubs, 1):
            print(idx, club.name)

    def display_active_or_upcoming_tournaments(self):
        """List all in-progress tournaments."""
        for idx, tourney in enumerate(self.tm.in_progress, 1):
            print(
                f"{idx}. {tourney.name} | {tourney.venue} | {tourney.dates.get('from')} - "
                f"{tourney.dates.get('to')}"
            )
            #
            # print(f"{idx}. {tourney.name} | {tourney.venue} | {tourney.dates.get("from")} - "
            #       f"{tourney.dates.get("to")}")
        # pass

    def get_command(self):
        """Prompt user for an action and return the corresponding command object."""
        while True:
            # 1 tournament → diretso view
            if len(self.tm.in_progress) == 1 and not self.view_club:
                return NoopCmd(
                    "tournament-view",
                    tournament=self.tm.in_progress[0],
                    clubs=self.cm.clubs,
                    tournament_manager=self.tm,
                    club_manager=self.cm
                )

            # >1 tournaments → list + choose
            elif len(self.tm.in_progress) > 1 and not self.view_club:

                while True:
                    print("Type C to create a new tournament or a tournament number to view/edit it.")
                    print("Type S to save all changes")
                    print("Type A to view the clubs")
                    print("Type X to exit.")
                    value = self.input_string()
                    if value.isdigit():
                        n = int(value)
                        if 1 <= n <= len(self.tm.in_progress):
                            return NoopCmd(
                                "tournament-view",
                                tournament=self.tm.in_progress[n - 1],
                                clubs=self.cm.clubs,
                                tournament_manager=self.tm,
                                club_manager=self.cm
                            )
                    elif value.upper() == "C":
                        return NoopCmd("create-tournament", club_manager=self.cm, tournament_manager=self.tm)
                    elif value.upper() == "S":
                        print("Saving changes...")
                        self.tm.save()
                        print("All changes saved!")
                    elif value.upper() == "A":
                        self.view_club = True
                        break  # go show clubs
                    elif value.upper() == "X":
                        return ExitCmd()

            # 0 tournaments or viewing clubs → clubs menu
            if self.view_club or len(self.tm.in_progress) == 0:
                self.view_club = True
                self.display_clubs()
                while True:
                    print("Type C to create a club or a club number to view/edit it.")
                    print("Type T to view in-progress tournaments")
                    print("Type X to exit.")
                    value = self.input_string()
                    if value.isdigit():
                        n = int(value)
                        if 1 <= n <= len(self.cm.clubs):
                            return NoopCmd("club-view", club=self.cm.clubs[n - 1])
                    elif value.upper() == "C":
                        return NoopCmd("club-create")
                    elif value.upper() == "T":
                        self.view_club = False
                        self.display_active_or_upcoming_tournaments()
                        break  # back to tournaments list (top of while)
                    elif value.upper() == "X":
                        return ExitCmd()
