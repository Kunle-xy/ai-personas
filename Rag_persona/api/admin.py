from django.contrib import admin
from .models import Document
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(Document)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'username')
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)