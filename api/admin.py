from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .auth import Student


class StudentAdmin(UserAdmin):
  list_display = ('username', 'email')
  search_fields = ('username', 'email')
  readonly_fields = ('date_joined', 'last_login')

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()


admin.site.register(Student, StudentAdmin)