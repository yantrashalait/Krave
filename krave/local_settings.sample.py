import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

from .settings import INSTALLED_APPS
INSTALLED_APPS += ['paypal.standard.ipn', 'social_django']

PAYPAL_TEST = True

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/user/profile/'
SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'user.pipeline.email_validate',
    'user.pipeline.create_role',
    'user.pipeline.create_profile',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY", "")
SOCIAL_AUTH_FACEBOOK_SECRET = ("SOCIAL_AUTH_FACEBOOK_SECRET", "")

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_APPLE_ID_CLIENT = os.environ.get("SOCIAL_AUTH_APPLE_ID_CLIENT", "")
SOCIAL_AUTH_APPLE_ID_TEAM = os.environ.get("SOCIAL_AUTH_APPLE_ID_TEAM", "")
SOCIAL_AUTH_APPLE_ID_KEY = os.environ.get("SOCIAL_AUTH_APPLE_ID_KEY", "")
SOCIAL_AUTH_APPLE_ID_SECRET = os.environ.get("SOCIAL_AUTH_APPLE_ID_SECRET", "")

STRIPE_SECRET_KEY = ''
STRIPE_PUBLISHABLE_KEY = ''

SEND_ACTIVATION_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 30
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SITE_URL = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# uncomment below in development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# use in deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')