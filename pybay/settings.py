import os
from base64 import b64decode

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

ADMINS = [('Simeon', 'simeonf@gmail.com')]

DEBUG = True
EMAIL_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    }
}

ALLOWED_HOSTS = []

CANONICAL_HOST = 'https://pybay.com'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Pacific"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = "some thing pybay2017 "

TEMPLATES = [{
    'APP_DIRS': True,
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PACKAGE_ROOT, 'templates')],
    'OPTIONS': {'context_processors': [
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.template.context_processors.request',
        'django.contrib.messages.context_processors.messages',
        'account.context_processors.account',
        'pinax_theme_bootstrap.context_processors.theme',
        'symposion.reviews.context_processors.reviews',
        'pybay.context_processors.settings_variables',
    ]}
}]

MIDDLEWARE_CLASSES = [
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]

ROOT_URLCONF = "pybay.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "pybay.wsgi.application"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.flatpages",

    # theme
    "bootstrapform",
    "pinax_theme_bootstrap",
    "pinax.boxes",

    # external
    "account",
    "easy_thumbnails",
    "eventlog",
    "django_markup",
    "markitup",
    "metron",
    "ordered_model",
    "taggit",
    "timezones",
    "columns",
    'django_generic_flatblocks',
    'django_generic_flatblocks.contrib.gblocks',


    # symposion
    "symposion.sponsorship",
    "symposion.conference",
    "symposion.speakers",
    "symposion.proposals",
    "symposion.schedule",
    "symposion.reviews",
    "symposion.teams",

    'pybay',
    'pybay.proposals',
    'pybay.faqs',
    'pybay.flatpages_ext.apps.FlatpagesExtConfig',
    'pybay.featured_speakers',
    'pybay.countdowns',
    'blockstuff',
    'crispy_forms',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
          'format': '%(asctime)s\n%(message)s'
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USER_DISPLAY = lambda user: user.email

AUTHENTICATION_BACKENDS = [
    # Use the simple django auth backend for now in PyBay
    'django.contrib.auth.backends.ModelBackend',

    # Permissions Backends
    "symposion.teams.backends.TeamPermissionsBackend",

    # Auth backends
    "account.auth_backends.EmailAuthenticationBackend",
]


MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_FILTER = ["symposion.markdown_parser.parse", {}]
MARKITUP_SKIN = "markitup/skins/simple"

CONFERENCE_ID = 1
SYMPOSION_PAGE_REGEX = r"(([\w-]{1,})(/[\w-]{1,})*)/"
PROPOSAL_FORMS = {
    "tutorial": "pybay.proposals.forms.TutorialProposalForm",
    "talk": "pybay.proposals.forms.TalkProposalForm",
}
#Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

SHOW_SPEAKERS_LIST_NAVBAR_LINK = False

DEBUG_TOOLBAR = False

PYBAY_API_TOKEN = "test"
API_TOKEN_PATH = '/home/pybay/api_token.txt'
if not os.environ.get('TRAVIS', False) and os.path.exists(API_TOKEN_PATH):
    with open(API_TOKEN_PATH) as f:
        PYBAY_API_TOKEN = f.read().strip() or PYBAY_API_TOKEN


ROLLBAR_PATH = '/home/pybay/rollbar.txt'
if not os.environ.get('TRAVIS', False) and os.path.exists(ROLLBAR_PATH):
    with open(ROLLBAR_PATH) as f:
        rollbar_token = f.read().strip()

    ROLLBAR = {
        'access_token': rollbar_token,
        'environment': 'development' if DEBUG else 'production',
        'branch': 'master',
        'root': BASE_DIR,
    }

    # Intentially added below the ROLLBAR const. Please do not move
    import rollbar
    rollbar.init(**ROLLBAR)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SENDGRID_PATH = '/home/pybay/sendgrid.txt'
if os.path.exists(SENDGRID_PATH):
    with open(SENDGRID_PATH) as f:
        sendgrid_password = f.read().strip()

        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        EMAIL_HOST = 'smtp.sendgrid.net'
        EMAIL_HOST_USER = 'pybay'
        EMAIL_HOST_PASSWORD = sendgrid_password
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        DEFAULT_FROM_EMAIL = 'info@pybay.com'

DEFAULT_FALLBACK_IMAGE = "new/img/unknown-speaker.png"

PROJECT_DATA = dict(
    cfp_close_date='June 17')
