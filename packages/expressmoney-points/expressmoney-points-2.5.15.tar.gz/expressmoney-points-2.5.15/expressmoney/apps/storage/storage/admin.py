from django.contrib import admin
from expressmoney.apps.storage.storage import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'name', 'type', 'is_public')
    list_filter = ('type', 'is_public')
    search_fields = ('=name', '=user_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['underwriter_id'].initial = request.user.id
            form.base_fields['underwriter_id'].disabled = True
            form.base_fields['user_id'].required = True
        return form
