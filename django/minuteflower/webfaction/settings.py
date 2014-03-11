# Django settings for minuteflower project.

import os
import decimal

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'minuteflower',
        'USER': 'minuteflower',
        'PASSWORD': '78f5fd56',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/minuteflower/webapps/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    'static',
    'media',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^zlc(^1v105m^2ej=_c(f(a85-kf*n%-i08e(c$wjz)gxxlyl='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'minuteflower.middleware.facebook.FacebookConnectMiddleware',
)

ROOT_URLCONF = 'minuteflower.urls'

TEMPLATE_DIRS = (
    'templates',
    '/home/minuteflower/webapps/django/minuteflower/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'minuteflower.userprofile',
    'minuteflower.gives',
    'minuteflower.api',
    'minuteflower.mfpaypal',
    'minuteflower.middleware',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/user/debug.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
         },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mf.api': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

GIVE_REPEAT_CHOICES = (
    ('day', 'Daily'),
    ('week', 'Weekly'),
    ('month', 'Monthly'),
)

PAYPAL_IPN_URL = 'paypal/ipn/eTeVSFqS/'

PAYPAL_RECEIVER_EMAIL = 'paypal@minuteflower.com'

PAYPAL_HEADERS = {
    'X-PAYPAL-SECURITY-USERID': 'paypal_api1.minuteflower.com',
    'X-PAYPAL-SECURITY-PASSWORD': '1366230421',
    'X-PAYPAL-SECURITY-SIGNATURE': 'AHGPPSO3b0RI7d31OEkMq5xKi81OAZT-0vKPpQQoQ9Cl2HkMxxKD-0vA',
    'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
    'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
    'X-PAYPAL-APPLICATION-ID': 'APP-80W284485P519543T',
}

PAYPAL_LIVE_HEADERS = {
    'X-PAYPAL-SECURITY-USERID': 'paypal_api1.minuteflower.com',
    'X-PAYPAL-SECURITY-PASSWORD': '6UL9H3K7HF94GNK4',
    'X-PAYPAL-SECURITY-SIGNATURE': 'AFcWxV21C7fd0v3bYYYRCpSSRl31AZEmb1F2YOrQOZTUaeHCdZu8s4YQ',
    'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
    'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
    'X-PAYPAL-APPLICATION-ID': 'APP-0R1011814A224973P',
}

PAYPAL_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

PAYPAL_MAX_PER_PAYMENT = 1000
PAYPAL_MAX_NUM_PAYMENTS = 1000
PAYPAL_MAX_TOTAL = 2000

#PAYPAL_FORM_URL = 'https://paypal.com/webscr'
PAYPAL_FORM_URL = 'https://sandbox.paypal.com/webscr'

PAYPAL_RETURN_URL = 'http://minuteflower.webfactional.com/'
PAYPAL_CANCEL_URL = PAYPAL_RETURN_URL

PAYPAL_PREAPPROVAL_DAYS = 365

# MinuteFlower commission is 3%
MF_COMMISION = decimal.Decimal(0.03)

IS_DEVELOPMENT = False

MIDDLEWARE_BLACKLIST = [
        '/favicon.ico'
        ]

DOMAIN = 'minuteflower.webfactional.com'

FACEBOOK_APP_ID = 273216792776884
FACEBOOK_APP_SECRET = 'ab5cd5ddfea09338c520f94b790d7459'

PASSWORD_SALT = 'P6juBMPbs0aqFxtGOr8ndA7v9uF4CprURqcI1kJ5RhGENyaxupk2htLyn4tIhNFc'

PHILANTHROPEDIA_API_KEY = 'minute_flower_api_key'
PHILANTHROPEDIA_API_URL = 'http://www.myphilanthropedia.org/api2/expert_reviews'
