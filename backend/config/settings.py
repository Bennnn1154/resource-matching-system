import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 關鍵修正 1: 從環境變數讀取 SECRET_KEY ---
# 這樣可以避免將密鑰暴露在程式碼中
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-z5o_3q3d*&ct=s2rlxlx(qq6w^_g-#t+n_u#pha=@%s8_byb47')

# --- 關鍵修正 2: 根據環境變數設定 DEBUG 模式 ---
# 在 Render 環境中，DEBUG 會自動變為 False，提高安全性
DEBUG = os.environ.get('DJANGO_ENV') != 'production'

# --- 關鍵修正 3: 設定 ALLOWED_HOSTS ---
# 這是解決 DisallowedHost 錯誤的核心
ALLOWED_HOSTS = [ #只有從以下網址visit的人可以瀏覽網頁，否則拒絕他的request
    'resource-matching-system-1.onrender.com',  # 您的後端網址
    'localhost',
    '127.0.0.1',
]

# Render 平台有時會透過這個環境變數提供它自己的主機名稱
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
]


# --- 關鍵修正 4: 修正 MIDDLEWARE ---
# 加入 whitenoise 並移除重複的項目
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# 這個設定告訴 collectstatic 指令，要將所有靜態檔案收集到哪裡。
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 這個設定是為了讓 Whitenoise 能更有效率地運作，是官方推薦的設定。
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- 關鍵修正 5: 修正 CORS_ALLOWED_ORIGINS ---
# 這裡應該要填入「前端」的網址，允許它來存取後端
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://resource-matching-system-2.onrender.com", # 您的前端網址
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}