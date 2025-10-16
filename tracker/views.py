from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST

from .models import Class, Student, Enrollment, Note
from django.urls import reverse

from .forms import ClassForm, EnrollStudentForm, StudentCreateForm


# ==================================================
# 1️⃣ HOME PAGE — LIST ALL CLASSES
# ==================================================
def class_list(request):
    """Display all classes."""
    classes = Class.objects.all().order_by('name')
    return render(request, 'tracker/class_list.html', {'classes': classes})


# ==================================================
# 2️⃣ CLASS DETAIL — SHOW ENROLLED STUDENTS
# ==================================================
def class_detail(request, class_id):
    """Show all students enrolled in a specific class."""
    classroom = get_object_or_404(Class, id=class_id)
    enrollments = (
        Enrollment.objects.filter(classroom=classroom)
        .select_related('student')
        .order_by('student__full_name')
    )
    return render(request, 'tracker/class_detail.html', {
        'classroom': classroom,
        'enrollments': enrollments,
    })


# ==================================================
# 3️⃣ CREATE A NEW CLASS
# ==================================================
def create_class(request):
    """Allow teachers to create a new class."""
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()

    return render(request, 'tracker/create_class.html', {'form': form})


# ==================================================
# 4️⃣ ENROLL EXISTING STUDENT INTO CLASS
# ==================================================
def enroll_student(request, class_id):
    """Enroll an existing student to a class."""
    classroom = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        form = EnrollStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            enrollment, created = Enrollment.objects.get_or_create(
                student=student, classroom=classroom
            )
            return redirect('class_detail', class_id=classroom.id)
    else:
        form = EnrollStudentForm()

    return render(request, 'tracker/enroll_student.html', {
        'form': form,
        'classroom': classroom
    })


# ==================================================
# 5️⃣ ADD NEW STUDENT & ENROLL TO CLASS
# ==================================================
def add_student(request, class_id):
    """Create a new student and enroll them in the class."""
    classroom = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            Enrollment.objects.get_or_create(student=student, classroom=classroom)
            return redirect('class_detail', class_id=classroom.id)
    else:
        form = StudentCreateForm()

    return render(request, 'tracker/add_student.html', {
        'form': form,
        'classroom': classroom
    })


# ==================================================
# 6️⃣ STUDENT DETAIL (Within Specific Class)
# ==================================================
def student_class_detail(request, class_id, student_id):
    """Show a student's notes & details for a specific class."""
    classroom = get_object_or_404(Class, id=class_id)
    student = get_object_or_404(Student, id=student_id)
    enrollment = get_object_or_404(Enrollment, classroom=classroom, student=student)
    notes = enrollment.notes.all().order_by('-updated_at')

    return render(request, 'tracker/student_class_detail.html', {
        'classroom': classroom,
        'student': student,
        'enrollment': enrollment,
        'notes': notes
    })


# ==================================================
# 7️⃣ NOTES
# ==================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Enrollment, Note

# =============================
# ADD NOTE
# =============================
@require_POST
def add_note(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    content = request.POST.get("content")

    if content:
        note = Note.objects.create(enrollment=enrollment, content=content)
        if request.headers.get("HX-Request"):
            return render(request, "tracker/note_block.html", {"note": note})
    return redirect("student_class_detail", classroom_id=enrollment.classroom.id, student_id=enrollment.student.id)


# =============================
# EDIT NOTE
# =============================
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.content = request.POST.get("content")
        note.save()
        if request.headers.get("HX-Request"):
            return render(request, "tracker/note_block.html", {"note": note})
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # For GET requests (when clicking ✏️ Edit)
    return render(request, "tracker/note_edit.html", {"note": note})


# =============================
# DELETE NOTE
# =============================
@require_POST
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return HttpResponse("")  # HTMX will remove element automatically


# ==================================================
# 8️⃣ GLOBAL STUDENT DIRECTORY
# ==================================================
def all_students(request):
    """Display all students and their enrolled classes."""
    students = (
        Student.objects.prefetch_related(
            Prefetch('enrollments', queryset=Enrollment.objects.select_related('classroom'))
        )
        .all()
        .order_by('full_name')
    )
    return render(request, 'tracker/all_students.html', {'students': students})


# ==================================================
# 9️⃣ GLOBAL STUDENT PROFILE (With All Classes)
# ==================================================
def global_student_detail(request, student_id):
    """View a student's global profile with all enrolled classes."""
    student = get_object_or_404(
        Student.objects.prefetch_related(
            Prefetch('enrollments', queryset=Enrollment.objects.select_related('classroom'))
        ),
        id=student_id,
    )
    return render(request, 'tracker/global_student_detail.html', {'student': student})


# ==================================================
# 🔟 LOAD NOTES FOR SPECIFIC CLASS (IN GLOBAL PROFILE)
# ==================================================
def load_notes_for_class(request, enrollment_id):
    """AJAX loader for showing notes when a class is selected in global student profile."""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    notes = enrollment.notes.all().order_by('-updated_at')
    return render(request, 'tracker/partials/note_list.html', {'notes': notes})

from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import StudentCreateForm

def add_student_global(request):
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # If it's an HTMX request, return a redirect trigger
            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response['HX-Redirect'] = reverse('all_students')
                return response
            return redirect('all_students')
    else:
        form = StudentCreateForm()

    return render(request, "tracker/partials/add_student_form.html", {"form": form})



# STUDENT EDIT

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentEditForm

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(next_url or 'all_students')
    else:
        form = StudentCreateForm(instance=student)

    return render(request, 'tracker/edit_student.html', {
        'form': form,
        'student': student,
        'next': next_url,
    })
