from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# Register your models here.

# Permite agregar usuarios con todos los campos necesarios desde el panel de admin
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email" ,"password1", "password2"),
            },
        ),
    )

admin.site.register(Usuario, CustomUserAdmin)
