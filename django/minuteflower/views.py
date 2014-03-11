from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings


def render_static(request, template_name):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))
