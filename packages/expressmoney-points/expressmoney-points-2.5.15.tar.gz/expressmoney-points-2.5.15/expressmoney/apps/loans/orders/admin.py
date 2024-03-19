from django.contrib import admin

from expressmoney.apps.loans.orders import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user_id', 'is_first_loan', 'is_first_order',
                    'amount_requested', 'amount_approved', 'period_approved',
                    'promocode_code', 'status', 'department_id')
    list_filter = ('created', 'status', 'is_first_loan', 'is_first_order', 'department_id')
    search_fields = ('=id', '=user_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
