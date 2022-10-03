DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'django_extensions',
    'rest_framework_simplejwt',
    'storages'
]
CUSTOM_APPS = [
    'sample_app.apps.SampleAppConfig',
    'user_app.apps.UserAppConfig'
]
