import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Configurações de email (para o formulário de contato)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Dev
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Produção

EMAIL_HOST = 'smtp.gmail.com'  # Ou seu servidor SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'leviesara@gmail.com'
EMAIL_HOST_PASSWORD = ''

DEFAULT_FROM_EMAIL = 'noreply@juridicflow.com'
CONTACT_EMAIL = 'contato@juridicflow.com'  # Email que receberá os contatos



SECRET_KEY = 'django-insecure-3eqkg6uqxij-jql9we%1%%4#jtiyelxa6p3#k(m(4x!w$)1j^9'

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    'corsheaders',

    # Custom Apps
    'apps.accounts',
    'apps.customers',
    'apps.deadlines',
    'apps.documents',
    'apps.finance',
    'apps.memberships',
    'apps.offices',
    'apps.organizations',
    'apps.processes',
    'apps.shared',
    'apps.landing',
    'apps.api',
]


JAZZMIN_SETTINGS = {
    # ===== IDENTIDADE =====
    "site_title": "JuridicFlow Platform",
    "site_header": "JuridicFlow",
    "site_brand": "JuridicFlow Admin",
    "welcome_sign": "Bem-vindo ao Painel da Plataforma",
    "copyright": "JuridicFlow © 2025",
    
    # ===== MENU LATERAL =====
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Ordem dos apps
    "order_with_respect_to": [
        "organizations",  # Primeiro o mais importante
        "offices",
        "memberships",
        "accounts",
        "customers",
        "processes",
        "deadlines",
        "documents",
    ],
    
    # ===== ÍCONES =====
    "icons": {
        # Accounts
        "accounts": "fas fa-users-cog",
        "accounts.User": "fas fa-user-shield",
        
        #processes
        "processes": "fas fa-gavel",
        "processes.Process": "fas fa-file-contract",
        "processes.ProcessParty": "fas fa-user-tie",

        #Financeiro
        "finance": "fas fa-dollar-sign",
        "finance.FeeAgreement": "fas fa-file-contract",
        "finance.Payment": "fas fa-money-bill-wave",

        # Organizations
        "organizations": "fas fa-building",
        "organizations.Organization": "fas fa-building",
        
        # Offices
        "offices": "fas fa-briefcase",
        "offices.Office": "fas fa-briefcase",
        
        # Memberships
        "memberships": "fas fa-id-badge",
        "memberships.Membership": "fas fa-id-card",

        #Customers
        "customers": "fas fa-users",
        "customers.Customer": "fas fa-user",

        # Deadlines
        "deadlines": "fas fa-clock",
        "deadlines.Deadline": "fas fa-bell",
        
        # Django padrão
        "auth": "fas fa-shield-alt",
        "auth.Group": "fas fa-users",

        # Documents
        "documents": "fas fa-folder",
        "documents.Document": "fas fa-file-pdf",
    },
    
    # ===== CUSTOMIZAÇÃO =====
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    
    # ===== LINKS NO TOPO =====
    "topmenu_links": [
        {"name": "Início", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Site", "url": "/", "new_window": True},
    ],
    
    # ===== SEGURANÇA =====
    # Ocultar apps que o Platform Admin não deve ver
    "hide_apps": [],
    
    # Ocultar models específicos
    "hide_models": [
        # Quando você tiver os models jurídicos, adicione aqui:
        # "customers.Customer",
        # "processes.Process",
        # "deadlines.Deadline",
        # "documents.Document",
    ],
    
    # ===== TEMA =====
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    
    # ===== LAYOUT =====
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.shared.middleware.OrganizationMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_USER_MODEL = 'accounts.User'

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


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configs API

# ===== REST FRAMEWORK =====
REST_FRAMEWORK = {
    # Autenticação
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Para browsable API
    ],
    
    # Permissões padrão
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Paginação
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    
    # Filtros
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Renderizadores
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Interface web (dev)
    ],
    
    # Schema (para documentação)
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Tratamento de erros
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    
    # Formato de data/hora
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}

# ===== JWT SETTINGS =====
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ===== CORS SETTINGS =====
# Para desenvolvimento
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Para produção (você vai configurar depois)
# CORS_ALLOWED_ORIGINS = [
#     "https://seudominio.com",
# ]

CORS_ALLOW_CREDENTIALS = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'JuridicFlow API',
    'DESCRIPTION': '''
    API REST completa para sistema jurídico multi-tenant.
    
    ## Autenticação
    
    Esta API utiliza JWT (JSON Web Tokens) para autenticação.
    
    ### Como autenticar:
    
    1. **Login**: POST /api/auth/login/
```json
       {
         "email": "seu@email.com",
         "password": "sua_senha"
       }
```
    
    2. **Usar o token**: Adicione o header em todas as requisições:
```
       Authorization: Bearer {seu_access_token}
```
    
    3. **Refresh token**: POST /api/auth/refresh/
```json
       {
         "refresh": "seu_refresh_token"
       }
```
    
    ## Recursos Principais
    
    - **Customers**: Gestão de clientes (PF/PJ)
    - **Processes**: Processos judiciais com partes e prazos
    - **Deadlines**: Prazos e compromissos com alertas
    - **Documents**: Upload e gestão de documentos
    - **Finance**: Contratos de honorários e pagamentos
    
    ## Multi-tenancy
    
    Todos os recursos são automaticamente filtrados pela organização e escritório
    do usuário autenticado. Não é necessário passar esses parâmetros manualmente.
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Componentes
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    
    # Autenticação
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    
    # Swagger UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
        'tryItOutEnabled': True,
        'docExpansion': 'none',
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
    },
    
    # Configurações de segurança
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
    'SECURITY': [{'Bearer': []}],
    
    # Tags
    'TAGS': [
        {'name': 'auth', 'description': 'Autenticação e gerenciamento de usuários'},
        {'name': 'customers', 'description': 'Gestão de clientes (PF/PJ)'},
        {'name': 'processes', 'description': 'Processos judiciais'},
        {'name': 'deadlines', 'description': 'Prazos e compromissos'},
        {'name': 'documents', 'description': 'Documentos e arquivos'},
        {'name': 'finance', 'description': 'Honorários e pagamentos'},
    ],
}