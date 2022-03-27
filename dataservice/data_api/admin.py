from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from data_api.models import *
from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportModelAdmin
from django.apps import apps


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class CustomSaveModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"
        ]
        self.exclude = ['created_user', 'updated_user']
        super(CustomSaveModelAdmin, self).__init__(model, admin_site)

    def save_model(self, request, obj, form, change):
        if obj is None:
            obj.created_user = request.user
        obj.updated_user = request.user
        obj.save()


class UserProfileAdmin(CustomModelAdmin):
    search_fields = ('company', 'role')


class StudentCourseStructureAdmin(CustomModelAdmin):
    search_fields = ('course_code', 'course_title')


class StructurePreferredCourseEnrollAdmin(CustomModelAdmin):
    search_fields = ('course_code', 'course_title')


class TransferringEquivalentCourseAdmin(CustomModelAdmin):
    search_fields = ('equivalent_type', 'name_committee1', 'advisor')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(StudentCourseStructure, StudentCourseStructureAdmin)
admin.site.register(StructurePreferredCourseEnroll,
                    StructurePreferredCourseEnrollAdmin)
admin.site.register(TransferringEquivalentCourse,
                    TransferringEquivalentCourseAdmin)
