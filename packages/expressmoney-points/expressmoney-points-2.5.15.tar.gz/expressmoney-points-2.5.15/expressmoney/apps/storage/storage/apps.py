from django.apps import AppConfig


class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expressmoney.apps.storage.storage'
    verbose_name = "Хранилище файлов"
