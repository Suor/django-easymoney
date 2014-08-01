INSTALLED_APPS = [
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db'
    },
}

SECRET_KEY = 'abc'
