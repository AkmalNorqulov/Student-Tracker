from django import forms
from .models import Class, Student


# ======================================================
# 🏫 CLASS CREATION FORM
# ======================================================
class ClassForm(forms.ModelForm):
    """Form for creating or editing a class."""

    class Meta:
        model = Class
        fields = ['name', 'subject', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter class name',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Subject (optional)',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional description...',
                }
            ),
        }


# ======================================================
# 👨‍🏫 ENROLL EXISTING STUDENT FORM
# ======================================================
class EnrollStudentForm(forms.Form):
    """Form for enrolling an existing student into a class."""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('full_name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select a student to enroll",
    )


# ======================================================
# 👩‍🎓 CREATE NEW STUDENT FORM
# ======================================================
class StudentCreateForm(forms.ModelForm):
    """Form for creating a new student."""
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'age']
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Full name',
                    'required': True,
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email (optional)',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Age (optional)',
                    'min': 1,
                }
            ),
        }
