import types

from django.http import HttpResponse

from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.utils.functional import curry

class DjangoJSONEncoder(JSONEncoder):

    def default(self, obj):

        # if it's a NoneType, return ""
        if type(obj) is types.NoneType:
            return Objectify("")

        # if it's a queryset, it's easy
        if isinstance(obj, QuerySet):
            return [Objectify(o) for o in obj]

        # maybe it's a normal object
        try:
            return JSONEncoder.default(self, obj)

        except TypeError, e:

            # maybe it's a Django object with an obj() method
            try:
                return obj.obj()
            except AttributeError:

                # maybe it's a Django object without an obj() method
                try:
                    return loads(serialize('json', [obj]))

                # OK, I give up
                except Exception, e:
                    return None

dumps = curry(dumps, cls=DjangoJSONEncoder)

'''
JSONify
-------
Turns an object that can be a conglomerate of Django and normal objects into
an HttpResponse containing a JSON serialized representation
'''
def JSONify(obj):
    return HttpResponse(dumps(obj))

'''
Objectify
---------
Turns an object that can be a conglomerate of Django and normal objects into
a JSON serialize-able object
'''
def Objectify(obj):
    return loads(dumps(obj))
