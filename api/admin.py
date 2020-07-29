from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .auth import Student
from .models import Class


class StudentAdmin(UserAdmin):
  list_display = ('username', 'email')
  search_fields = ('username', 'email')
  readonly_fields = ('date_joined', 'last_login')

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()


class ClassAdmin(admin.ModelAdmin):
  list_display = ['class_name', 'class_year', 'average_rating', ]
  search_fields = ['class_name', 'class_year']


admin.site.register(Student, StudentAdmin)
admin.site.register(Class, ClassAdmin)

