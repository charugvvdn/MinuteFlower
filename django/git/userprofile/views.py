import logging

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

from reportlab.pdfgen import canvas

from django.contrib.auth.models import User

from minuteflower.gives.models import Give, Transaction

from minuteflower.api import JSONify

from minuteflower.userprofile.forms import *
from minuteflower.mfpaypal import paypal_preapproval

logger = logging.getLogger('mf.api')

def can_give(request):
    return JSONify(request.user.get_profile().can_give())


@login_required
def api_change_password(request):
    try:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            return JSONify(form.save(request))
        else:
            print form.errors
    except Exception, e:
        print str(e)
        return JSONify(False)
    return JSONify(False)

def api_loggedin(request):
    return JSONify(request.user.is_authenticated())

def api_login(request):
    try:
        user = authenticate(username=request.POST.get('username'),
                password=request.POST.get('password'))
        login(request, user)
        return JSONify(request.user.is_authenticated())
    except Exception, e:
        print str(e)
    return JSONify(request.user.is_authenticated())


def api_logout(request):
    logout(request)
    return JSONify(not request.user.is_authenticated())


def api_register(request):
    logger.debug("api_register")
    logout(request)
    form = None
    if request.method == 'POST':
        form = UserEmailCreationForm(request.POST)
        logger.debug("form_isvalid = %s" % form.is_valid())
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return JSONify({ 'success': request.user.is_authenticated() })
    return JSONify({ 'success': False, 'error': form.errors })


def update_settings(request):
    form = UpdateSettingsForm(request.POST)
    if form.is_valid():
        return JSONify(form.save(request))
    return JSONify(False)


def register(request, template_name):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

def perform_payments(request, template_name):
    if request.method == 'POST':
        request.user.get_profile().perform_payments()
    return render_to_response(template_name, {}, context_instance=RequestContext(request))

def logged_in(request):
    return JSONify(request.user.is_authenticated())

def api_get_settings(request):
    try:
        profile = request.user.get_profile()
        profile.update_pp_preapproval()
        profile.update_favorite_charities()
        profile.update_favorite_gives()
        if not profile.pp_preapproval_key_approved and profile.pp_email:
            profile.pp_preapproval_key = paypal_preapproval(profile.pp_email)
            profile.save()
        return JSONify({
            'salary': str(profile.salary),
            'minute_value': str(profile.minute_value),
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'pp_preapproval_key': profile.pp_preapproval_key,
            'pp_preapproval_key_approved': profile.pp_preapproval_key_approved,
            'pp_email': profile.pp_email,
            'pp_preapproval_url': settings.PAYPAL_FORM_URL + '?cmd=_ap-preapproval&preapprovalkey=%s' % profile.pp_preapproval_key,
            'favorite_charities': profile.detail_favorite_charities,
            'favorite_gives': profile.detail_favorite_gives,
            })
    except Exception, e:
        return JSONify(str(e))

def report(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=report.pdf'

    p = canvas.Canvas(response)

    p.drawString(100, 750, "Report for %s" % request.user.username)

    line_height = 30
    y = 750 - line_height
    for transaction in Transaction.objects.filter(cashed_in=True, give__user=request.user):
        give = transaction.give
        p.drawString(100, y, "[%s] %s - %d minute[s] - $%.2f" % (
            str(transaction.time_start),
            give.charity.name,
            round(give.hours_per_give()*60,0),
            round(float(transaction.minute_value)*give.hours_per_give()*60),
        ))
        y -= line_height

    p.showPage()
    p.save()
    return response
