import datetime
import logging
from django import forms
from minuteflower.gives.models import *

logger = logging.getLogger('mf.api')

class CreateGiveForm(forms.Form):
    time_start = forms.DateTimeField()
    duration = forms.IntegerField() # in minutes
    repeat = forms.CharField()
    charity = forms.ModelChoiceField(queryset=Charity.objects.all())
    now = forms.BooleanField(required=False)
    give_name = forms.CharField()

    def clean(self):
        cd = super(CreateGiveForm, self).clean()
        if cd.get('now'):
            logger.debug("in the now")
            cd['time_start'] = datetime.datetime.utcnow()
        else:
            logger.debug("scheduled give")
        return cd

    def save(self, request):
        cd = self.cleaned_data
        if not request.user.is_authenticated():
            return None
        g = Give(
                user=request.user,
                time_start=cd['time_start'],
                time_end=cd['time_start'] + datetime.timedelta(0, cd['duration']*60),
                repeat=cd['repeat'],
                charity=cd['charity'],
                give_name=cd['give_name'],
        )
        g.save()
        return g

class DeleteGiveForm(forms.Form):
    give = forms.ModelChoiceField(queryset=Give.objects.all())

    def save(self, request):
        cd = self.cleaned_data
        if cd['give'].user == request.user:
            cd['give'].delete()
            return True
        return False

class UpdateGiveForm(forms.Form):
    time_start = forms.DateTimeField()
    duration = forms.IntegerField() # in minutes
    repeat = forms.CharField()
    now = forms.BooleanField(required=False)
    give_name = forms.CharField()
    give_id = forms.IntegerField()

    def clean(self):
        cd = super(UpdateGiveForm, self).clean()
        if cd.get('now'):
            cd['time_start'] = datetime.datetime.utcnow()
        return cd

    def save(self, request):
        cd = self.cleaned_data
        give = Give.objects.get(id=cd['give_id'])

        give.time_start=cd['time_start']
        give.time_end=cd['time_start'] + datetime.timedelta(0, cd['duration']*60)
        give.repeat=cd['repeat']
        give.give_name = cd['give_name']
        give.save()

        return give  
