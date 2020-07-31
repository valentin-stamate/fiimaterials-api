from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .auth import Student
from .models import Class, UsefulLink, StudentRating


class StudentAdmin(UserAdmin):
  list_display = ('username', 'email')
  search_fields = ('username', 'email')
  readonly_fields = ('date_joined', 'last_login')

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()


class ClassAdmin(admin.ModelAdmin):
  list_display = ['class_name', 'class_year', 'average_rating', 'votes_number']
  search_fields = ['class_name', 'class_year']


class UsefulLinkAdmin(admin.ModelAdmin):
  list_display = ['name']
  search_fields = ['name', 'type']


class StudentRatingAdmin(admin.ModelAdmin):
  list_display = ['student', 'class_name', 'rating']
  search_fields = ['student', 'class_name']


admin.site.register(Student, StudentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(UsefulLink, UsefulLinkAdmin)
admin.site.register(StudentRating, StudentRatingAdmin)