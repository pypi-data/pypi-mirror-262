from django.contrib import admin

from expressmoney.apps.scoring.pdl_ru import models


@admin.register(models.FeatureStore)
class FeatureStoreAdmin(admin.ModelAdmin):
    list_display = ('order_id',
                    'order_created',
                    'amount_requested',
                    'amount_approved',
                    'user_id',
                    'passport_serial',
                    'passport_number',
                    'loan_id',
                    'loan_status',
                    'loan_status_date',
                    'em_total_loans',
                    'em_interests_sum',
                    'nbki_score',
                    'accounts_total_mfo_3y',
                    'xml',
                    'is_from_scoring',
                    'is_refilled',
                    )
    search_fields = ('=order_id', 'passport_number',)
    list_filter = ('order_created', 'loan_status', 'is_from_scoring', 'is_refilled')

    ordering = ('-order_created',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False