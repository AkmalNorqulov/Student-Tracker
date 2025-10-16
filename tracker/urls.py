from django.urls import path
from . import views

urlpatterns = [
    # ======================================================
    # 📘 CLASS MANAGEMENT
    # ======================================================
    path('', views.class_list, name='class_list'),
    path('classes/create/', views.create_class, name='create_class'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),

    # ------------------------------------------------------
    # 👨‍🏫 STUDENT ENROLLMENT / CREATION (per class)
    # ------------------------------------------------------
    path('class/<int:class_id>/add-student/', views.add_student, name='add_student'),
    path('class/<int:class_id>/enroll-student/', views.enroll_student, name='enroll_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),


    # ------------------------------------------------------
    # 🧍 STUDENT DETAIL (within specific class)
    # ------------------------------------------------------
    path(
        'class/<int:class_id>/student/<int:student_id>/',
        views.student_class_detail,
        name='student_class_detail',
    ),

    # ======================================================
    # 📝 NOTE MANAGEMENT (AJAX / HTMX)
    # ======================================================
    path("enrollments/<int:enrollment_id>/add-note/", views.add_note, name="add_note"),
    path("edit-note/<int:note_id>/", views.edit_note, name="edit_note"),
    path("delete-note/<int:note_id>/", views.delete_note, name="delete_note"),

    # ======================================================
    # 🌍 GLOBAL STUDENT DIRECTORY
    # ======================================================
    path('students/', views.all_students, name='all_students'),
    path('student/<int:student_id>/', views.global_student_detail, name='global_student_detail'),

    # ------------------------------------------------------
    # 🔁 LOAD NOTES (used dynamically in global profile)
    # ------------------------------------------------------
    path(
        'student/load-notes/<int:enrollment_id>/',
        views.load_notes_for_class,
        name='load_notes_for_class',
    ),

    path("students/add/", views.add_student_global, name="add_student_global"),

]