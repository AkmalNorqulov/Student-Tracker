from django.db import models
from django.utils import timezone


# ======================================================
# 📘 CLASS MODEL
# ======================================================
class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['name']

    def __str__(self):
        return self.name


# ======================================================
# 🧍 STUDENT MODEL
# ======================================================
class Student(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    address = models.TextField(blank=True, null=True)

    # Many-to-many through Enrollment
    classes = models.ManyToManyField('Class', through='Enrollment', related_name='students')

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


# ======================================================
# 🧾 ENROLLMENT MODEL (Intermediate)
# ======================================================
class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='enrollments'
    )
    classroom = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='enrollments'
    )
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'classroom')
        ordering = ['classroom__name', 'student__full_name']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.full_name} → {self.classroom.name}"


# ======================================================
# 📝 NOTE MODEL
# ======================================================
class Note(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name='notes'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"Note for {self.enrollment.student.full_name} in {self.enrollment.classroom.name}"

    def short_content(self):
        return (
            f"{self.content[:50]}..."
            if len(self.content) > 50
            else self.content
        )
