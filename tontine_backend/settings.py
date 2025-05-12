import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-bbpx$vlubc6$uid(zer4wccxot%cypnxxrr#+j*x(sc#q8yc+h'

DEBUG = True

ALLOWED_HOSTS = []

# 🔌 Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion_tontine',
    'tailwind',
    'theme',
   
]

# ⚙️ Nom de l'app Tailwind
TAILWIND_APP_NAME = 'theme'

# ✅ Autorisation IP pour debug_toolbar
INTERNAL_IPS = ['127.0.0.1']

# 🔐 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]

ROOT_URLCONF = 'tontine_backend.urls'

# 📁 Répertoires des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tontine_backend', 'theme', 'templates'),
            os.path.join(BASE_DIR, 'gestion_tontine', 'templates'),  # <--- Ajout important
        ],
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

WSGI_APPLICATION = 'tontine_backend.wsgi.application'

# 🛢️ Configuration base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tontine_db',
        'USER': 'root',
        'PASSWORD': 'mamou',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 🔐 Validation des mots de passe
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

# 🌍 Localisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

# 🖼️ Fichiers statiques (CSS, JS, etc.)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "gestion_tontine" / "static",  # <- corrigé ici (underscore)
]

# 👤 Django redirige ici si l'utilisateur n'est pas connecté
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'gestion_tontine:dashboard'  # Redirige vers le dashboard après la connexion


# 🗝️ Type de clé primaire
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🛠️ NPM pour Tailwind
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"


