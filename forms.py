from django import forms
from .models import Student, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration', 'contact', 'document']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present']

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class ReportForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
        label='Aluno'
    )
    start_date = forms.DateField(required=False, label='Data Inicial')
    end_date = forms.DateField(required=False, label='Data Final')