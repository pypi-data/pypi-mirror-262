from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import ForeignKey

from expressmoney.apps.loans.accounting import models


@admin.register(models.LoanIssueOperation)
class LoanIssueOperationAdmin(admin.ModelAdmin):
    list_display = ('created', 'loan', 'amount', 'balance', 'payment_id')
    list_filter = ('created',)
    search_fields = ('=loan__id', '=payment_id')
    readonly_fields = ('balance',)
    formfield_overrides = {
        ForeignKey: {'widget': AdminTextInputWidget},
    }

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.LoanInterestsOperation)
class LoanInterestsOperationAdmin(LoanIssueOperationAdmin):
    list_display = ('created', 'loan', 'amount', 'balance', 'payment_id')
    list_filter = ('created',)
    search_fields = ('=loan__id', '=payment_id')
    readonly_fields = ('balance',)
    formfield_overrides = {
        ForeignKey: {'widget': AdminTextInputWidget},
    }


@admin.register(models.LoanInterestsPaymentOperation)
class LoanInterestsPaymentAdmin(LoanIssueOperationAdmin):
    pass


@admin.register(models.LoanBodyPaymentOperation)
class LoanBodyPaymentOperationAdmin(LoanIssueOperationAdmin):
    pass
