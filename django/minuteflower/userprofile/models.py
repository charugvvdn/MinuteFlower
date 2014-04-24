import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

from minuteflower.mfpaypal import paypal_pay, paypal_mock_pay

from decimal import Decimal

from minuteflower.mfpaypal import paypal_preapproval_details

from minuteflower.gives.models import Give, Transaction, Charity

from minuteflower.models import CurrencyField


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    salary = CurrencyField(decimal_places=2, max_digits=19, null=True, blank=True, default=0)
    minute_value = CurrencyField(decimal_places=2, max_digits=19, null=True, blank=True, default=0)
    fbid = models.BigIntegerField(null=True, blank=True)

    pp_email = models.EmailField(max_length=255, blank=True)
    pp_preapproval_key = models.TextField(blank=True)
    pp_preapproval_key_approved = models.BooleanField(blank=True)
    favorite_charities = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.user.__unicode__()

    def valid_pp_preapproval(self):
        if not self.pp_preapproval_key:
            return False
        return self.pp_preapproval_key_approved

    def update_pp_preapproval(self):
        if not self.pp_preapproval_key:
            return False
        preapproval = paypal_preapproval_details(self.pp_preapproval_key)
        self.pp_preapproval_key_approved = preapproval.get('approved', 'false') == 'true'
        self.save()

    def can_give(self):
        return self.pp_preapproval_key_approved

    def create_transactions(self):
        for give in Give.objects.filter(user=self.user):
            dates = give.dates_to_present()
            dates.sort()
            for date in dates:
                if (not give.transactioned_date) or date > give.transactioned_date:
                    Transaction(
                        give=give,
                        minute_value=self.minute_value,
                        time_start=date,
                        cashed_in=False
                    ).save()
                    give.transactioned_date = date
                    give.save()

    def perform_payments(self):
        for transaction in Transaction.objects.filter(cashed_in=False, give__user=self.user):
            give = transaction.give
            # handle payment
            if settings.DEBUG:
                print 'Payment in process: %s is paying %f to %s' % (give.user.username, give.amount_per_give(), give.charity.paypal_email)
            pay = paypal_pay(
                give.amount_per_give(),
                give.user.get_profile().pp_preapproval_key,
                give.user.get_profile().pp_email,
                give.charity.paypal_email,
                'MinuteFlower donation to %s' % give.charity.name
            )
            if pay.get('responseEnvelope', {}).get('ack', '') == 'Success':
                transaction.cashed_in = True
                transaction.save()

    def update_favorite_charities(self):
        self.detail_favorite_charities = []
        list = self.favorite_charities.split(',')
        list = filter(None, list)
        for charity in Charity.objects.filter(id__in=list):
            self.detail_favorite_charities.append(charity.obj1(favorite_charities=self.favorite_charities))
        
    def update_favorite_gives(self):
        self.detail_favorite_gives = Give.objects.filter(user=self.user).order_by('-time_start')[:3]


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
