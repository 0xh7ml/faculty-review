from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from .models import Faculty, Course, Review


class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'short_name', 'department', 'designation', 'created_at', 'updated_at')


class CourseResource(resources.ModelResource):
    faculties = fields.Field(
        column_name='faculties',
        attribute='faculties',
        widget=ManyToManyWidget(Faculty, field='name', separator=',')
    )
    class Meta:
        model = Course
        fields = ('id', 'name', 'code', 'old_code', 'faculties', 'created_at', 'updated_at')


class ReviewResource(resources.ModelResource):
    faculty = fields.Field(
        column_name='faculty',
        attribute='faculty',
        widget=ForeignKeyWidget(Faculty, 'name')
    )
    class Meta:
        model = Review
        fields = ('id', 'faculty', 'course', 'behavior', 'lecture', 'grading', 'rating', 'created_at', 'updated_at')


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    resource_class = FacultyResource
    list_display = ('name', 'short_name', 'department', 'designation')


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('name', 'code', 'old_code')


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
    list_display = ('faculty', 'course', 'behavior', 'lecture', 'grading', 'rating')