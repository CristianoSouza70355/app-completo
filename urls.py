from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('alunos/', views.student_list, name='student_list'),
    path('frequencia/', views.attendance_register, name='attendance_register'),
    path('aluno/<int:student_id>/editar/', views.edit_student, name='edit_student'),
    path('aluno/<int:student_id>/excluir/', views.delete_student, name='delete_student'),
    path('marcar-frequencia/', views.mark_attendance, name='mark_attendance'),
    path('gerar-relatorio/', views.generate_report, name='generate_report'),
]