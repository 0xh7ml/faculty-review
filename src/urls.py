from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faculty/<int:faculty_id>/review/', views.SubmitReview, name='submit_review'),
    path('courses/', views.CourseView, name='courses'),
]