from django.contrib import admin
from .models import Mails, File


from .models import Mails, File, MailAuthorization, Email


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class MailAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    list_display = ('theme', 'author', 'date_send', 'date_take')
    search_fields = ('theme', 'description')


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1


class MailAuthorizationAdmin(admin.ModelAdmin):
    inlines = [EmailInline]
    list_display = ('user', 'email_verified')
    search_fields = ('user__username', 'user__email')


admin.site.register(Mails, MailAdmin)
admin.site.register(MailAuthorization, MailAuthorizationAdmin)
