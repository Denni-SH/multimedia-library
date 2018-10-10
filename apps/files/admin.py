from django.contrib import admin
from .models import UserFile

class UserFileAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(UserFile, UserFileAdmin)