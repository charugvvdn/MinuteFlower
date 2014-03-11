from django.conf import settings
from urllib import urlopen
from django.utils.simplejson import load


def pull_charity_data(ein):
    if not ein:
        return None
    endpoint = "%s?ein=%s&apikey=%s" % (settings.PHILANTHROPEDIA_API_URL,
        ein, settings.PHILANTHROPEDIA_API_KEY)
    response = urlopen(endpoint)
    return load(response)
