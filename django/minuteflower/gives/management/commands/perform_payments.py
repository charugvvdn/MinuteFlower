import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from minuteflower.gives.models import Give

from mfpaypal import paypal_pay, paypal_mock_pay

class Command(BaseCommand):
    help = "Performs payments that haven't been performed yet"

    def handle(self, *args, **options):

        if len(args) == 1:
            users = User.objects.filter(id=int(args[0]))
        else:
            users = User.objects.all()

        for user in users:
            user.get_profile().perform_payments()
