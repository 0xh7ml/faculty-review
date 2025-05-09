from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Faculty(models.Model):
    PROGRAM_CHOICES = [
        ('BSME', 'BSME'),      # Bachelor of Science in Mechanical Engineering
        ('BCSE', 'BCSE'),      # Bachelor of Computer Science and Engineering
        ('BSCE', 'BSCE'),      # Bachelor of Science in Civil Engineering
        ('BEEE', 'BEEE'),      # Bachelor of Electrical and Electronic Engineering
        ('BBA', 'BBA'),        # Bachelor of Business Administration
        ('BTHM', 'BTHM'),      # Bachelor of Tourism and Hospitality Management
        ('BSAg', 'BSAg'),      # Bachelor of Science in Agriculture
        ('BAEng', 'BAEng'),    # Bachelor of Arts in English
        ('BAEcon', 'BAEcon'),  # Bachelor of Arts in Economics
        ('BSN', 'BSN'),        # Bachelor of Science in Nursing
    ]
    FACULTY_DESIGNATIONS = [
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Senior Lecturer', 'Senior Lecturer'),
        ('Lecturer', 'Lecturer'),
    ]
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    department = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    designation = models.CharField(max_length=50, choices=FACULTY_DESIGNATIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"
        ordering = ['name']
        db_table = 'tb_faculty'

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    old_code = models.CharField(max_length=10, null=True, blank=True)
    faculties = models.ManyToManyField(Faculty, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['code']
        db_table = 'tb_course'

    def __str__(self):
        return self.name
    
class Review(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    behavior = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3)
        ],
        default=1,
    )
    lecture = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3)
        ],
        default=1,
    )
    grading = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=1,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Calculate the average rating
        self.rating = (self.behavior + self.lecture + self.grading) / 3
        super().save(*args, **kwargs)
    
    def update_rating(self):
        # Calculate the average rating
        self.rating = (self.behavior + self.lecture + self.grading) / 3
        self.save()
        
    # Update the rating field in the database
        self.faculty.update_rating()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        db_table = 'tb_review'

    def __str__(self):
        return f"{self.faculty} - {self.rating}"