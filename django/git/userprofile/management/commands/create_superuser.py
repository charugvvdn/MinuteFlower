from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates a superuser - user/pass = a/p"

    def handle(self, *args, **options):
        u = User(username='a', email='a@b.com', is_superuser=True,
                is_staff=True)
        u.save()
        u.set_password('p')
        u.save()
