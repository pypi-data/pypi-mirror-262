from django.contrib import admin

from expressmoney.apps.loans.loans import models


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'status', 'order',
                    'extended_end_date')
    list_filter = ('status', 'created')
    search_fields = ('=id', '=order__id', '=order__user_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
