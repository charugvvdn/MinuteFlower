import datetime
import decimal

from dateutil import relativedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.utils.simplejson import loads, dumps

from minuteflower.api import Objectify
from minuteflower.models import CurrencyField


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
            blank=True,
            upload_to='category_imags',
            max_length=255)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.image:
            return '/static/%s' % self.image.name
        else:
            return '/static/img/default-category.png'

    def obj(self):
        ret = loads(serialize('json', [self]))
        ret[0]['derived'] = {
            'image_url': self.image_url()
        }
        return ret


class Charity(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    paypal_email = models.EmailField()
    image = models.ImageField(blank=True,
            upload_to='charity_imgs',
            max_length=255)
    hero_image = models.ImageField(blank=True,
            upload_to='charity_imgs',
            max_length=255)
    category = models.ForeignKey(Category)
    is_featured = models.BooleanField(blank=False)

    # Philanthropedia Fields
    ein = models.CharField(max_length=31, blank=True)
    philanthropedia_name = models.CharField(max_length=255, blank=True)
    social_cause = models.CharField(max_length=255, blank=True)
    org_type = models.CharField(max_length=31, blank=True)
    research_url = models.URLField(blank=True)
    medal_year = models.PositiveIntegerField(blank=True, null=True)
    medal_url = models.URLField(blank=True)
    guidestar_id = models.CharField(max_length=31, blank=True)
    public_report_url = models.URLField(blank=True)
    thumbs_up = models.PositiveIntegerField(null=True, blank=True)
    thumbs_down = models.PositiveIntegerField(null=True, blank=True)
    reviews_impact = models.CharField(max_length=4095, blank=True)
    reviews_strengths = models.CharField(max_length=4095, blank=True)
    reviews_toimprove = models.CharField(max_length=4095, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.image:
            return '/static/%s' % self.image.name
        else:
            return '/static/img/default-charity.png'

    def category_image_url(self):
        return self.category.image_url()

    def category_name(self):
        return self.category.name

    def obj(self):
        ret = loads(serialize('json', [self]))
        ret[0]['derived'] = {
            'image_url': self.image_url(),
            'category_image_url': self.category_image_url(),
            'category_name': self.category_name(),
        }
        return ret

    def obj1(self, favorite_charities):
	ret = self.obj()
        ret[0]['derived']['is_favorite'] = str(self.id) in favorite_charities
        return ret

    
class Review(models.Model):
    REVIEW_TYPES = (
        ('IM', 'Impact'),
        ('ST', 'Strengths'),
        ('AR', 'Areas for Improvement'),
    )
    review_type = models.CharField(max_length=2, choices=REVIEW_TYPES, blank=True)
    label = models.CharField(max_length=127, blank=True)
    charity = models.ForeignKey(Charity)
    expert_type = models.CharField(max_length=63, blank=True)
    comment = models.CharField(max_length=4095)

    def __unicode__(self):
        return "%d: %s - %s: %s" % (self.id, self.charity.__unicode__(), self.label, self.comment[0:15])


class Give(models.Model):
    user = models.ForeignKey(User)
    charity = models.ForeignKey(Charity)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(null=True)
    repeat = models.CharField(max_length=10,
            choices=settings.GIVE_REPEAT_CHOICES)
    cashed_in_date = models.DateTimeField(null=True)
    transactioned_date = models.DateTimeField(null=True)
    end_date = models.DateField(null=True)
    give_name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%d: %s (%s) --> %s" % (self.id, self.user.__unicode__(), self.give_name, self.charity.__unicode__())

    def obj(self):
        ret = loads(serialize('json', [self]))
        ret[0]['derived'] = {
            'charity_name': self.charity.name,
            'charity_description': self.charity.description,
            'charity_image': self.charity.category_image_url(),
            'duration': int(
                    (self.time_end - self.time_start).total_seconds() / 60),
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return ret

    def hours_per_give(self):
        return (self.time_end - self.time_start).total_seconds() / 60 / 60

    def amount_per_give(self):
        return decimal.Decimal(self.hours_per_give()) * self.user.get_profile().minute_value * 60

    def dates_to_present(self):
        if self.time_start > datetime.datetime.utcnow():
            return []
        ret = [self.time_start]
        if self.repeat == 'day':
            while ret[0] + datetime.timedelta(1) < datetime.datetime.utcnow():
                ret.insert(0, ret[0] + datetime.timedelta(1))
            return ret
        if self.repeat == 'month':
            while ret[0] + relativedelta.relativedelta(months=1) \
                    < datetime.datetime.utcnow():
                ret.insert(0, ret[0] + \
                        relativedelta.relativedelta(months=1))
            return ret
        if self.repeat == 'week':
            while ret[0] + datetime.timedelta(7) \
                    < datetime.datetime.utcnow():
                ret.insert(0, ret[0] + datetime.timedelta(7))
            return ret
        return ret

    def time_to_present(self):
        dates = self.dates_to_present()
        ret = len(dates) * \
                (self.time_end - self.time_start).total_seconds()
        for date in dates:
            end_time = \
                date + datetime.timedelta(seconds = \
                        (self.time_end - self.time_start).total_seconds())
            if end_time > datetime.datetime.utcnow():
                ret -= (end_time - datetime.datetime.utcnow()).total_seconds()
        return ret

    def next_give(self):
        ret = self.time_start
        if self.repeat == 'day':
            while ret < datetime.datetime.utcnow():
                ret += datetime.timedelta(1)
        if self.repeat == 'week':
            while ret < datetime.datetime.utcnow():
                ret += datetime.timedelta(7)
        if self.repeat == 'month':
            while ret < datetime.datetime.utcnow():
                ret += relativedelta.relativedelta(months=1)
        if ret > datetime.datetime.utcnow():
            if (not self.repeat==True) or \
                    (self.end_date and \
                    self.end_date > datetime.datetime.utcnow().date()):
                return ret
        return None


class Transaction(models.Model):
    give = models.ForeignKey(Give)
    minute_value = CurrencyField(decimal_places=2, max_digits=19)
    time_start = models.DateTimeField()
    cashed_in = models.BooleanField()

    def __unicode__(self):
        return self.give.__unicode__()


class Flower(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
            blank=True,
            upload_to='flower_imgs',
            max_length=255)
    rule = models.TextField()

    # be very careful! flower.rule gets passed into eval()
    # it assumes the existence of the local var 'user'
    # it should return a boolean True / False

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.image:
            return '/static/%s' % self.image.name
        else:
            return '/static/img/default-flower.png'

    def achieved_by(self, user):
        return eval(self.rule)
