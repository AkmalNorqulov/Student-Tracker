from django.contrib import admin
from .models import Class, Student, Enrollment, Note


# ======================================================
# 📝 INLINE CONFIGURATIONS
# ======================================================
class NoteInline(admin.TabularInline):
    """Inline for adding notes directly under Enrollment."""
    model = Note
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


class EnrollmentInline(admin.TabularInline):
    """Inline for managing student enrollments."""
    model = Enrollment
    extra = 1
    autocomplete_fields = ['student', 'classroom']


# ======================================================
# 🏫 CLASS ADMIN
# ======================================================
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    search_fields = ('name', 'subject')
    inlines = [EnrollmentInline]


# ======================================================
# 👩‍🎓 STUDENT ADMIN
# ======================================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'age', 'created_at')
    search_fields = ('full_name', 'email')
    inlines = [EnrollmentInline]


# ======================================================
# 🧾 ENROLLMENT ADMIN
# ======================================================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'joined_at')
    search_fields = ('student__full_name', 'classroom__name')
    list_filter = ('classroom',)
    inlines = [NoteInline]


# ======================================================
# 🗒 NOTE ADMIN
# ======================================================
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'short_content', 'updated_at')
    search_fields = (
        'enrollment__student__full_name',
        'enrollment__classroom__name',
        'content',
    )
    readonly_fields = ('created_at', 'updated_at')
