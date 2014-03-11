import urllib2
import datetime
import json

from django.conf import settings

def paypal_request(url, get_vars):
    get_vars = '&'.join(['%s=%s' % (k,v) for (k,v) in get_vars.iteritems()])
    return json.loads(urllib2.urlopen(
            urllib2.Request("%s?%s" % (url, get_vars), headers=settings.PAYPAL_HEADERS)
            ).read())

#
#   paypal_preapproval
#   ------------------
#   Returns preapprovalKey
#
def paypal_preapproval(sender_email):
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(days=settings.PAYPAL_PREAPPROVAL_DAYS)
    preapproval = paypal_request(
            "https://svcs.sandbox.paypal.com/AdaptivePayments/Preapproval", {
                'cancelUrl': settings.PAYPAL_CANCEL_URL,
                'currencyCode': 'USD',
                'endingDate': end.strftime(settings.PAYPAL_TIME_FORMAT),
                'maxAmountPerPayment': settings.PAYPAL_MAX_PER_PAYMENT,
                'maxNumberOfPayments': settings.PAYPAL_MAX_NUM_PAYMENTS,
                'maxTotalAmountOfAllPayments': settings.PAYPAL_MAX_TOTAL,
                'pinType': 'NOT_REQUIRED',
                'requestEnvelope.errorLanguage': 'en_US',
                'returnUrl': settings.PAYPAL_RETURN_URL,
                'startingDate': start.strftime(settings.PAYPAL_TIME_FORMAT),
                'senderEmail': sender_email,
            })
    if settings.DEBUG:
        print 'paypal_preapproval:'
        import pprint
        pprint.pprint(preapproval)
    return preapproval.get('preapprovalKey', '')


def paypal_preapproval_details(preapproval_key):
    preapproval = paypal_request(
            "https://svcs.sandbox.paypal.com/AdaptivePayments/PreapprovalDetails", {
                'requestEnvelope.errorLanguage': 'en_US',
                'preapprovalKey': preapproval_key,
            })
    if settings.DEBUG:
        print 'paypal_preapproval_details:'
        import pprint
        pprint.pprint(preapproval)
    return preapproval


def paypal_mock_pay(amount, preapproval_key, sender_email, receiver_email, memo):
    print amount
    print preapproval_key
    print sender_email
    print receiver_email
    print memo

def paypal_pay(amount, preapproval_key, sender_email, receiver_email, memo):
    if settings.DEBUG:
        print 'paypal_pay:'
        import pprint
        pprint.pprint(preapproval_key)
    memo = memo.replace(' ', '+')
    pay = paypal_request(
            "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay", {
                'actionType': 'PAY',
                'cancelUrl': settings.PAYPAL_CANCEL_URL,
                'currencyCode': 'USD',
                'feesPayer': 'EACHRECEIVER',
                'memo': memo,
                'preapprovalKey': preapproval_key,
                'receiverList.receiver(0).amount': round(amount * settings.MF_COMMISION, 2),
                'receiverList.receiver(0).email': settings.PAYPAL_RECEIVER_EMAIL,
                'receiverList.receiver(0).primary': 'false',
                'receiverList.receiver(1).amount': round(amount, 2),
                'receiverList.receiver(1).email': receiver_email,
                'receiverList.receiver(1).primary': 'true',
                'requestEnvelope.errorLanguage': 'en_US',
                'returnUrl': settings.PAYPAL_RETURN_URL,
                'reverseAllParallelPaymentsOnError': 'true',
                'senderEmail': sender_email,
            })
    if settings.DEBUG:
        print 'paypal_pay:'
        import pprint
        pprint.pprint(pay)
    return pay
