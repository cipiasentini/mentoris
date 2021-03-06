"""
Django settings for Tutorias project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ao)f9&a_tif!hdk5esd9j#ewpbnihzn6+u25_h9eduj=-go+tv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/login'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django_select2',
    'bootstrap_datepicker_plus',
    'sysacad',
    'menu',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Tutorias.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Tutorias.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

if (sys.platform == 'darwin'):
    DATABASES = {
        'default': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'TUTORIAS_DATOS',
            'HOST': '0.0.0.0',
            'PORT': '1402',
            'USER': 'SA',
            'PASSWORD': 'Tutori@s2018',
            'OPTIONS': {
                'driver': 'ODBC Driver 13 for SQL Server',
                # 'driver': 'FreeTDS',
            }
        },
        'sysacad': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'SYSACAD',
            'HOST': '0.0.0.0',
            'PORT': '1401',
            'USER': 'sysacadTutoriasLogin',
            'PASSWORD': 'Tutori@s2018',
            'OPTIONS': {
                # 'driver': 'FreeTDS',
                # 'provider': 'SQLNCLI11',
                'driver': 'ODBC Driver 13 for SQL Server',
            }
        }
        # Es importante que para que se puedan migrar las bases de datos de legado del sysacad se cree
        # un usuario y login cuyo default schema sea Sysacad y se le agregue los permisos correspondientes

        # En la default no es necesario ya que el schema por defecto es dbo y ahi es donde se crean
        # las tablas para esa base de datos con el usuario SA
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'TUTORIAS_DATOS',
            'HOST': 'DESKTOP-SIRB7DH',
            'PORT': '',
            'USER': 'TutorAdmin',
            'PASSWORD': 'Tutori@s2018',
            'OPTIONS': {
                'driver': 'ODBC Driver 13 for SQL Server',
            }
        },
        'sysacad': {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'SYSACAD',
            'HOST': 'DESKTOP-SIRB7DH',
            'PORT': '',
            'USER': 'SysacadAdmin',
            'PASSWORD': 'Tutori@s2018',
            'OPTIONS': {
                'driver': 'ODBC Driver 13 for SQL Server',
            }
        }
        # Es importante que para que se puedan migrar las bases de datos de legado del sysacad se cree
        # un usuario y login cuyo default schema sea Sysacad y se le agregue los permisos correspondientes

        # En la default no es necesario ya que el schema por defecto es dbo y ahi es donde se crean
        # las tablas para esa base de datos con el usuario SA
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# PARA LA BD

DATABASE_ROUTERS = ['Tutorias.TutoriasRouter.TutoriasRouter']


# PARA SELECT2

SELECT2_JS = '/static/js/select2.min.js'
SELECT2_CSS = '/static/css/select2.min.css'
