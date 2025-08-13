from commands.context import Context
from models import ClubManager
from models import TournamentManager

from .base import BaseCommand


class ClubListCmd(BaseCommand):
    """Command to get the list of clubs"""

    def execute(self):
        cm = ClubManager()
        tm = TournamentManager(club_manager=cm)
        return Context("main-menu", club_manager=cm, tournament_manager=tm)
