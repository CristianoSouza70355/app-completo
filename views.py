from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Student, Attendance
from .forms import StudentForm, AttendanceForm, LoginForm, ReportForm
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json
from django.views.decorators.http import require_http_methods

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == 'APAE':
                request.session['is_logged'] = True
                return redirect('student_list')
            else:
                messages.error(request, 'SENHA INCORRETA')
    else:
        form = LoginForm()
    return render(request, 'attendance/login.html', {'form': form})

def student_list(request):
    if not request.session.get('is_logged'):
        return redirect('login')
    
    students = Student.objects.all()
    form = StudentForm()
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
            
    return render(request, 'attendance/student_list.html', {
        'students': students,
        'form': form
    })

def edit_student(request, student_id):
    if not request.session.get('is_logged'):
        return redirect('login')
        
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'attendance/edit_student.html', {
        'form': form,
        'student': student
    })

def attendance_register(request):
    if not request.session.get('is_logged'):
        return redirect('login')
        
    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        is_present = request.POST.get('is_present') == 'True'
        
        student = get_object_or_404(Student, id=student_id)
        Attendance.objects.update_or_create(
            student=student,
            date=date,
            defaults={'is_present': is_present}
        )
        
    students = Student.objects.all()
    return render(request, 'attendance/attendance_register.html', {
        'students': students
    })

@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        is_present = data.get('is_present')
        date = data.get('date')

        try:
            student = Student.objects.get(id=student_id)
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                date=date,
                defaults={'is_present': is_present}
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def generate_report(request):
    student_name = request.GET.get('student_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    query = Attendance.objects.all()
    if student_name:
        query = query.filter(student__name__icontains=student_name)
    if start_date:
        query = query.filter(date__gte=start_date)
    if end_date:
        query = query.filter(date__lte=end_date)

    # Criar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_frequencia.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [['Nome', 'Data', 'Situação']]
    for attendance in query:
        data.append([
            attendance.student.name,
            attendance.date.strftime('%d/%m/%Y'),
            'Presente' if attendance.is_present else 'Ausente'
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response

def export_pdf(request):
    # Implementação da geração do PDF aqui
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    # Adicionar conteúdo ao PDF
    p.save()
    
    return response


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return JsonResponse({'success': True})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Aluno não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
