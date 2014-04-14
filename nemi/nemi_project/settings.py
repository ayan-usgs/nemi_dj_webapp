''' Module contains Django settings for nemi project. All sensitive settings and
server specific settings should be in the local_settings module which is not under version control
In particular any constant that contains passwords or resources that vary depending on the server should
go in the local_settings module. This module will contain fallback resources for all essential settings.
Note that this module expects additional apps or middleware to be defined in local_settings with the
constants ADDITIONAL_APPS and ADDITIONAL_MW_CLASSES, respectively.
'''

import os

PROJECT_HOME = os.path.dirname(__file__)
SITE_HOME = os.path.split(PROJECT_HOME)[0]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Mary Bucknell', 'mbucknell@usgs.gov'),
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# The real database should be defined in local_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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

TEST_RUNNER = 'nemi_project.test_runner.ManagedModelTestRunner'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_HOME, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = ((os.path.join(PROJECT_HOME, 'static'),)
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

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "django.core.context_processors.request",
                               "common.context_processors.project_settings",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'nemi_project.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'nemi_project.urls'

TEMPLATE_DIRS = (
                 os.path.join (PROJECT_HOME, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.flatpages',
    
    # third party apps
    'tinymce',
    'rest_framework',
    'djangojs',
    
    # NEMI/CIDA specific apps
    'common',
    'newsfeed',
    'domhelp',
    'methods',
    'protocols',
    'sams',
#	'memo',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SESSION_COOKIE_AGE = 28800 # In seconds, this is eight hours


#NEMI defined settings
NEW_ACCOUNT_NOTIFICATIONS = () # List of emails to send new account notifications to.
WQP_URL = "http://www.waterqualitydata.us"
# Code to be used for google analytics. If tracking is desired for a server, set to the track code in local_settings.py.
GA_TRACKING_CODE = ''

try:
    ADDITIONAL_APPS = ()
    ADDITIONAL_MW_CLASSES = ()
    from local_settings import *
except ImportError:
    # add apps to this variable for this specific server configuration
    pass

# Add any apps and middleware classes defined in local_settings
if ADDITIONAL_APPS:
    INSTALLED_APPS += ADDITIONAL_APPS
    
if ADDITIONAL_MW_CLASSES:
    MIDDLEWARE_CLASSES += ADDITIONAL_MW_CLASSES

# Set security based on whether DEBUG is on
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
    
# Set up TinyMCE configuration
TINYMCE_JS_URL = STATIC_URL + 'lib/tiny_mce/tiny_mce.js'

TINYMCE_DEFAULT_CONFIG = {
    'theme' : "advanced",
}

if os.getenv('JENKINS_URL', False):
    JENKINS_TASKS = (
                    'django_jenkins.tasks.with_coverage',
                     )
    JENKINS_TEST_RUNNER = 'nemi_project.test_jenkins_runner.ManagedModelTestRunner'
    INSTALLED_APPS += ('django_jenkins', 'jasmine',)
    PROJECT_APPS = (
        'common', 
        'jasmine',
        'methods', 
        'protocols', 
        'sams', 
        'newsfeed', 
        'domhelp',
    )
    DATABASES['default'].update(dict(
            ENGINE=os.getenv('DBA_SQL_DJANGO_ENGINE'),
            USER=os.getenv('DBA_SQL_ADMIN'),
            PASSWORD=os.getenv('DBA_SQL_ADMIN_PASSWORD'),
            HOST=os.getenv('DBA_SQL_HOST'),
            PORT=os.getenv('DBA_SQL_PORT')
            ))
    