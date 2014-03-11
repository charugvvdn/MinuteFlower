import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Creates transactions for gives that have happened"

    def handle(self, *args, **options):

        if len(args) == 1:
            users = User.objects.filter(id=int(args[0]))
        else:
            users = User.objects.all()

        for user in users:
            user.get_profile().create_transactions()
