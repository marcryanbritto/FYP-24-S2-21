# DiseaseRiskCalcultor/settings.py

INSTALLED_APPS = [
    ...
    'DiseaseRiskCalculator',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Redirect to home page after login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
