from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import ugettext_lazy as _

from . import models

#: override system settings
admin.site.site_header = _(u"WellPlayed TV - Face Check")
admin.site.index_title = _(u"Administration")

#: append additional settings
UserAdmin.list_display += ('is_verified', )
UserAdmin.list_filter += ('is_verified', )
UserAdmin.fieldsets += (
    (_('Face check'), {'fields': ('is_verified', )}),
)
UserAdmin.list_editable = ('is_verified', )


class SecretAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'updated_at')


admin.site.register(models.Secret, SecretAdmin)
admin.site.register(models.User, UserAdmin)
