from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import OneToOneField

from expressmoney.apps.profiles.profiles import models


@admin.register(models.RussianProfile)
class RussianProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_profile', 'last_name', 'first_name', 'middle_name', 'birth_place', 'birth_date',
                    'is_identified', 'is_verified', 'passport_serial', 'passport_number', 'snils')
    search_fields = ('=user_profile__user_id',
                     '=passport_serial',
                     '=passport_number',
                     '=last_name',
                     'snils',
                     '=first_name',
                     '=middle_name',
                     )

    readonly_fields = ('user_profile', 'is_identified', 'is_verified', 'credit_score',
                       'credit_score_created', 'is_read_only', 'is_verified_date', 'sign_date', )

    formfield_overrides = {OneToOneField: {'widget': AdminTextInputWidget}, }

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            self.readonly_fields = ('is_identified', 'is_verified', 'is_verified_date', 'sign_date',
                                    'credit_score', 'credit_score_created', 'is_read_only',
                                    )
        return super().get_readonly_fields(request, obj)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            last_name, first_name, middle_name = search_term.split()
            queryset = self.model.objects.filter(first_name=first_name,
                                                 last_name=last_name,
                                                 middle_name=middle_name)
        except ValueError:
            pass
        return queryset, use_distinct

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
