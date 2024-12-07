from django.contrib import admin
from .models import *
import pandas as pd
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.templatetags.static import static

class ExamMarkInline(admin.TabularInline):
    model = ExamMark
    extra = 1
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            section_id = request.resolver_match.kwargs.get('object_id')
            if section_id:
                kwargs['queryset'] = Student.objects.filter(sections__id=section_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [ExamMarkInline]

class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id')
    search_fields = ['first_name', 'last_name']

class ExamMarkAdmin(admin.ModelAdmin):  
    list_display = ('student', 'first_mark', 'second_mark', 'third_mark', 'subject', 'section')
    search_fields = ['student__first_name', 'student__last_name']


# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ExamMark, ExamMarkAdmin )
admin.site.register(Announce)
admin.site.register(Home)
admin.site.register(Course)
admin.site.register(Image)
admin.site.register(HomeWork)
admin.site.register(UserProfile)
admin.site.register(Subject)
admin.site.register(ExamCorrection)
admin.site.register(Classe)

