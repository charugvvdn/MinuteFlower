import datetime
import calendar
import logging
import collections

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from minuteflower.api import JSONify

from minuteflower.gives.models import Give, Charity, Category
from minuteflower.gives.forms import *

logger = logging.getLogger('mf.api')

def create_give(request):
    try:
        form = CreateGiveForm(request.POST)
        if form.is_valid():
            g = form.save(request)
            return JSONify(g)
        else:
            logger.debug("CREATE ERROR %s" % form.errors)
            print form.errors
            return HttpResponse(form.errors)
    except Exception, e:
        return HttpResponse(str(e))


def delete_give(request):
    try:
        form = DeleteGiveForm(request.POST)
        if form.is_valid():
            return JSONify(form.save(request))
        return JSONify(False)
    except Exception, e:
        return HttpResponse(str(e))

def update_give(request):
    logger.debug("update_give")
    try:
        form = UpdateGiveForm(request.POST)
        if form.is_valid():
            logger.debug("update_give, form is valid")
            return JSONify(form.save(request))
        logger.debug("update_give OOPS!")
        return JSONify(False)
    except Exception, e:
        logger.debug("update_give borked - %s", str(e))
        return HttpResponse(str(e))

def list_gives(request):
    gives = Give.objects.filter(user=request.user)

    return JSONify(gives)

def list_social_gives(request):
    gives = Give.objects.exclude(user=request.user).order_by('-time_start')
    return JSONify(gives)

def show_give(request, id):
    return JSONify(get_object_or_404(Give, id=id))


def list_charities(request, category_id=None):
    if category_id:
        return JSONify(Charity.objects.filter(category=category_id))

    favorite_charities=request.user.get_profile().favorite_charities
    ret = []
    for charity in Charity.objects.all():
	ret.append(charity.obj1(favorite_charities=favorite_charities))
    return JSONify(ret)

def list_featured_charities(request):
    return JSONify(Charity.objects.filter(is_featured=True))

def show_charity(request, id):
    charity = Charity.objects.filter(id=id)[0].obj1(favorite_charities=request.user.get_profile().favorite_charities)
    return JSONify(charity)


def list_categories(request):
    return JSONify(Category.objects.all())


def my_donations(request):
    res = []
    for charity in Charity.objects.all():
        gives = Give.objects.filter(user=request.user, charity=charity)
        if gives.count() > 0:

            total_time = sum([g.time_to_present() for g in gives])

            last_give = gives[0].time_start
            last_give_id = gives[0].id
            for give in gives.filter(time_start__lt = datetime.datetime.utcnow()):
                dates = give.dates_to_present()
                if dates[0] > last_give:
                    last_give = dates[0]
                    last_give_id = give.id

            next_give = None
            for give in gives:
                if (not next_give) or (give.next_give() and give.next_give() < next_give):
                    next_give = give.next_give()

            if last_give and last_give < datetime.datetime.utcnow():
                last_give = str(calendar.timegm(last_give.timetuple()))
            else:
                last_give = None
            if next_give:
                next_give = str(calendar.timegm(next_give.timetuple()))

            res.append({
                'charity': charity,
                'last_give': last_give,
                'total_time': int(total_time / 60),
                'next_give': next_give,
                'last_give_id': last_give_id
            })
    return JSONify(res)


def my_causes(request):
    ret = []
    for category in Category.objects.all():
        total_time = 0
        for charity in Charity.objects.filter(category=category):
            for give in Give.objects.filter(user=request.user, charity=charity):
                total_time += len(give.dates_to_present()) * \
                        (give.time_end - give.time_start).total_seconds()
        ret.append({
            'category': category,
            'color': category.color,
            'total_time': total_time,
        })
    return JSONify(ret)


def my_gives(request):
    ret = {}
    for give in Give.objects.filter(user=request.user, time_start__lt=datetime.datetime.utcnow()).order_by('-time_start'):
	k = str(give.time_start.year) + ':' + str(give.time_start.month)
	if k in ret:
	    d = ret[k]
	else:
	    d = []
	    ret[k] = d
	d.append(give)

    rret = collections.OrderedDict(sorted(ret.items(),reverse=True))

    return JSONify(rret)

def my_scheduled_gives(request):
    repeat_list = ['day','month','week']
    return JSONify(Give.objects.filter(user=request.user, repeat__in = ['day','week','month']).order_by('time_start'))
    #return JSONify(Give.objects.filter(user=request.user, time_start__gt=datetime.datetime.utcnow()).order_by('time_start'))

def time_status(request, include_previous=True):
    total_time = 0
    try:
        if include_previous:
            for give in Give.objects.filter(user=request.user):
                total_time += len(give.dates_to_present()) * \
                        (give.time_end - give.time_start).total_seconds()

        cur_gives = []
        for give in Give.objects.filter(user=request.user):
            for date in give.dates_to_present():
                end_time = date + datetime.timedelta(seconds=(give.time_end - give.time_start).total_seconds())
                if end_time > datetime.datetime.utcnow():
                    cur_gives.append((end_time - datetime.datetime.utcnow()).total_seconds())
                    if include_previous:
                        total_time -= (end_time - datetime.datetime.utcnow()).total_seconds()
                    else:
                        total_time += (give.time_end - give.time_start).total_seconds() - (end_time - datetime.datetime.utcnow()).total_seconds()


        return JSONify({
            'seconds':  '%.2d' % (total_time % 60),
            'minutes':  '%.2d' % (((total_time - (total_time % 60)) / 60) % 60),
            'hours':    '%.2d' % ((total_time - (total_time % (60*60))) / (60*60)),
            'cur_gives': cur_gives,
            'total_time': total_time,
        })
    except Exception, e:
        return JSONify({'error':str(e)})
