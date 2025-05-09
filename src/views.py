from django.shortcuts import render
from .models import Faculty, Course, Review
from django.db.models import Avg, Prefetch
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    faculties_list = Faculty.objects.annotate(
        avg_rating=Avg('reviews__rating'),
    ).prefetch_related('courses')
    
    context = {
        'faculties': faculties_list,
    }
    return render(request, 'index.html', context)

def CourseView(request):
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses.html', context)


def SubmitReview(request, faculty_id):
    ...
