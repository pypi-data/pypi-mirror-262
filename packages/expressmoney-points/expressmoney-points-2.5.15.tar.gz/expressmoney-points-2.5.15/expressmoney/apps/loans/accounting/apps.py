from django.apps import AppConfig


class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expressmoney.apps.loans.accounting'
    verbose_name = "Бухгалтерия"
