from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .auth import Student
from .models import Class, Link, ClassRating, Resource, Feedback


class StudentAdmin(UserAdmin):
  list_display = ('username', 'email')
  search_fields = ('username', 'email')
  readonly_fields = ('date_joined', 'last_login')

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()


class ClassAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'name_short', 'year', 'average_rating', 'votes_number']
  search_fields = ['name', 'year']
  readonly_fields = ['updated_at']


class LinkAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
  search_fields = ['name']


class ClassRatingAdmin(admin.ModelAdmin):
  list_display = ['student', 'class_name', 'rating']
  search_fields = ['student', 'class_name']


class ResourceAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'tag_list']
  search_fields = ['title', 'tag_list']


class FeedbackAdmin(admin.ModelAdmin):
  list_display = ['id', 'student', 'name', 'feedback']


admin.site.register(Student, StudentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(ClassRating, ClassRatingAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Feedback, FeedbackAdmin)
