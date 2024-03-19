from django.contrib import admin

from expressmoney.apps.scoring.cache import models


@admin.register(models.NBKIScore)
class NBKIScoreAdmin(admin.ModelAdmin):
    list_display = ('created',
                    'first_name',
                    'last_name',
                    'passport_serial',
                    'passport_number',
                    'score',
                    )
    search_fields = ('=passport_number',)
    list_filter = ('created', )
    ordering = ('-created',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(models.NBKICreditHistory)
class NBKICreditHistoryAdmin(admin.ModelAdmin):
    list_display = ('created',
                    'first_name',
                    'last_name',
                    'passport_serial',
                    'passport_number',
                    'total_accounts_mfo_new',
                    'total_accounts_mfo_old',
                    )
    search_fields = ('=passport_number',)
    list_filter = ('created', )
    ordering = ('-created',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(models.NBKICreditHistoryV2)
class NBKICreditHistoryV2Admin(admin.ModelAdmin):
    list_display = ('created',
                    'first_name',
                    'last_name',
                    'passport_serial',
                    'passport_number',
                    'accounts_total_mfo_3y',
                    'accounts_zero',
                    'accounts_pastdue_mfo',
                    'balance_pastdue_mfo',
                    'time'
                    )
    search_fields = ('=passport_number',)
    list_filter = ('created', )
    # ordering = ('-created',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
