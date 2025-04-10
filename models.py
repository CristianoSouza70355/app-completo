from django.db import models

class Student(models.Model):
    name = models.CharField('Nome', max_length=100)
    registration = models.CharField('Matrícula', max_length=20, unique=True)
    contact = models.CharField('Contato', max_length=50, blank=True, null=True)
    document = models.CharField('Documento', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField('Data')
    is_present = models.BooleanField('Presente')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        unique_together = ['student', 'date']
