import os


def get_db_config():
    from expressmoney.google import get_secret
    is_local = False if os.getenv('GAE_APPLICATION') else True

    db_host = get_secret('DB_HOST')
    db_user = get_secret('DB_USER')
    db_password = get_secret('DB_PASSWORD')
    db_host_auth = get_secret('DB_HOST_AUTH')
    db_user_auth = get_secret('DB_USER_AUTH')
    db_password_auth = get_secret('DB_PASSWORD_AUTH')

    db_user_scoring = get_secret('DB_USER_SCORING')
    db_password_scoring = get_secret('DB_PASSWORD_SCORING')

    databases = {
        'auth_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1' if is_local else db_host_auth,
            'PORT': '5432',
            'NAME': 'auth',
            'USER': db_user_auth,
            'PASSWORD': db_password_auth,
            'CONN_MAX_AGE': 60,
        },
        'loans_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1' if is_local else db_host,
            'PORT': '5432',
            'NAME': 'loans',
            'USER': db_user,
            'PASSWORD': db_password,
            'CONN_MAX_AGE': 60,
            # 'ATOMIC_REQUESTS': True,  # IMPORTANT: DO NOT ENABLE FOR CRITICAL ENDPOINTS (PAYMENTS, ACCOUNTING)
        },
        'profiles_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1' if is_local else db_host,
            'PORT': '5432',
            'NAME': 'profiles',
            'USER': db_user,
            'PASSWORD': db_password,
            'CONN_MAX_AGE': 60,
        },
        'storage_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1' if is_local else db_host,
            'PORT': '5432',
            'NAME': 'storage',
            'USER': db_user,
            'PASSWORD': db_password,
            'CONN_MAX_AGE': 60,
            'ATOMIC_REQUESTS': True,  # IMPORTANT: DO NOT ENABLE FOR CRITICAL ENDPOINTS (PAYMENTS, ACCOUNTING)
        },
        'scoring_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1' if is_local else db_host,
            'PORT': '5432',
            'NAME': 'scoring',
            'USER': db_user_scoring,
            'PASSWORD': db_password_scoring,
            'CONN_MAX_AGE': 60,
        },

    }
    return databases
