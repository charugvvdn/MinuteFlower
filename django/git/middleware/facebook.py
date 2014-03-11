import hashlib
import time
import random
import urlparse
import json

from urllib2 import urlopen, URLError, HTTPError
from datetime import datetime

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from minuteflower.userprofile.models import UserProfile

def get_password(fbuser):
    return hashlib.md5('$'.join([settings.PASSWORD_SALT, fbuser['id']])).hexdigest()

class FacebookConnectMiddleware(object):
    
    def process_request(self, request):
        if settings.IS_DEVELOPMENT:
            return
    
        print 'middleware: ' + request.path

        if request.path in settings.MIDDLEWARE_BLACKLIST:
            print 'path blacklisted'
            return

        if request.user.is_authenticated():
            print 'already authed'
            if request.path == '/login/facebook/':
                if request.user.get_profile().fbid:
                    print 'already have fbid'
                    return HttpResponseRedirect('/')
        print 'not already authed'
        if request.path == '/login/facebook/':
            print 'trying to log in'
            request.session['has_tried_fb_login'] = True
            if not 'code' in request.GET:
                print 'doing the code thing'
                request.session['state'] = random.randint(0,10000)
                dialogUrl = "https://www.facebook.com/dialog/oauth?client_id=%(appid)s&redirect_uri=%(uri)s&state=%(state)s" % {
                    'appid':    settings.FACEBOOK_APP_ID,
                    'uri':      'http://%s/login/facebook/' % settings.DOMAIN,
                    'state':    request.session['state'],
                }
                return HttpResponseRedirect(dialogUrl)
        if 'code' in request.GET and 'state' in request.GET and 'state' in request.session:
            print 'code and state and shit is here'
            print request.session['state']
            print request.GET['state']
            if not int(request.session['state']) == int(request.GET['state']):
                return
            print 'states match'
            tokenUrl = "https://graph.facebook.com/oauth/access_token?client_id=%(appid)s&redirect_uri=%(uri)s&client_secret=%(secret)s&code=%(code)s" % {
                'appid':    settings.FACEBOOK_APP_ID,
                'uri':      'http://%s/login/facebook/' % settings.DOMAIN,
                'secret':   settings.FACEBOOK_APP_SECRET,
                'code':     request.GET['code'],
            }
            print tokenUrl
            try:
                response = urlopen(tokenUrl).read()
            except HTTPError, e:
                print('http error')
                return
            except URLError, e:
                print('url error')
                return
            print response
            params = urlparse.parse_qs(response)
            print params
            graphUrl = "https://graph.facebook.com/me?access_token=%(token)s" % {'token': params['access_token'][0]}
            print graphUrl
            try:
                fbuser = json.loads(urlopen(graphUrl).read())
            except HTTPError, e:
                print('http error')
                return
            except URLError, e:
                print('url error')
                return
            
            print 'aha we have a user'
            print fbuser
            
            if UserProfile.objects.filter(fbid=int(fbuser['id'])).count() == 0 and not request.user.is_authenticated():
                print 'registering user'

                user = User(username=fbuser['id'])
                user.save()
                user.get_profile().fbid = int(fbuser['id'])
                user.get_profile().name = fbuser['name']
                user.get_profile().save()
                user.set_password(get_password(fbuser))
                user.save()
                print 'user registered'
            print 'now getting user'
            if request.user.is_authenticated():
                user = request.user
                user.get_profile().fbid = int(fbuser['id'])
                user.get_profile().name = fbuser['name']
                user.get_profile().save()
            else:
                user = authenticate(username=fbuser['id'], password=get_password(fbuser))
            print user
            if user:
                if not request.user.is_authenticated():
                    print 'now logging in user'
                    login(request, user)
                    print 'logged in user'
                return HttpResponseRedirect('/')
            else:
                print "didn't get a user"
