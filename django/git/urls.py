from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import django.contrib.auth.views
import minuteflower.views
import minuteflower.userprofile.views
import minuteflower.gives.views

urlpatterns = patterns('',
    url(r'^$', minuteflower.views.render_static, {'template_name': 'index.html'}),

    url(r'^api/category/$', minuteflower.gives.views.list_categories),
    url(r'^api/category/(?P<category_id>\d+)/charity/$', minuteflower.gives.views.list_charities),

    url(r'^api/charity/$', minuteflower.gives.views.list_charities),
    url(r'^api/charity/(?P<id>\d+)/$', minuteflower.gives.views.show_charity),
    url(r'^api/charity/featured/$', minuteflower.gives.views.list_featured_charities),

    url(r'^api/give/$', minuteflower.gives.views.list_gives),
    url(r'^api/give/social/$', minuteflower.gives.views.list_social_gives),
    url(r'^api/give/(?P<id>\d+)/$', minuteflower.gives.views.show_give),
    url(r'^api/give/create/$', minuteflower.gives.views.create_give),
    url(r'^api/give/delete/$', minuteflower.gives.views.delete_give),
    url(r'^api/give/update/$', minuteflower.gives.views.update_give),

    url(r'^api/give/mydonations/$', minuteflower.gives.views.my_donations),
    url(r'^api/give/mycauses/$', minuteflower.gives.views.my_causes),
    url(r'^api/give/mygives/$', minuteflower.gives.views.my_gives),
    url(r'^api/give/mygives/scheduled/$', minuteflower.gives.views.my_scheduled_gives),
    url(r'^api/give/timestatus/$', minuteflower.gives.views.time_status),
    url(r'^api/give/timestatus/nowonly/$', minuteflower.gives.views.time_status, {'include_previous': False}),

    url(r'^api/loggedin/$', minuteflower.userprofile.views.api_loggedin),
    url(r'^api/login/$', minuteflower.userprofile.views.api_login),
    url(r'^api/register/$', minuteflower.userprofile.views.api_register),
    url(r'^api/logout/$', minuteflower.userprofile.views.api_logout),

    url(r'^api/user/password/$', minuteflower.userprofile.views.api_change_password),
    url(r'^api/user/settings/update/$', minuteflower.userprofile.views.update_settings),
    url(r'^api/user/settings/$', minuteflower.userprofile.views.api_get_settings),
    url(r'^api/user/loggedin/$', minuteflower.userprofile.views.logged_in),
    url(r'^api/user/cangive/$', minuteflower.userprofile.views.can_give),

    url(r'^login/$',  django.contrib.auth.views.login, {'template_name':'user/login.html'}),
    url(r'^login/facebook/$',  minuteflower.views.render_static, {'template_name':'facebook_login.html'}),
    url(r'^logout/$', django.contrib.auth.views.logout, {'template_name':'user/logout.html'}),
    url(r'^register/$', minuteflower.userprofile.views.register, {'template_name':'user/register.html'}),
    url(r'^pay/$', minuteflower.userprofile.views.perform_payments, {'template_name':'user/perform_payments.html'}),
    url(r'^report/$', minuteflower.userprofile.views.report),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
