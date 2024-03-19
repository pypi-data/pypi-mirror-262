from django.contrib import admin

from expressmoney.apps.loans.promocodes import models


@admin.register(models.PromocodeDescription)
class PromocodeDescriptionAdmin(admin.ModelAdmin):
    list_display = ('created', 'updated', 'code', 'is_active', 'product', 'valid_from', 'valid_to', 'total',
                    'activated', 'comment')
    readonly_fields = ('activated',)
    search_fields = ('=code',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('created', 'code', 'user_id', 'promocode_description')
    list_filter = ('created',)
    search_fields = ('=code', '=user_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
