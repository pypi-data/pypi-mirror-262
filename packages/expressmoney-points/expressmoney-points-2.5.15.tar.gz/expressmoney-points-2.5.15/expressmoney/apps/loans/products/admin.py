from django.contrib import admin

from expressmoney.apps.loans.products import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'is_active', 'free_period', 'interests')
    list_filter = ('is_active',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
