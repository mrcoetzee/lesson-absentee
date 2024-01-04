import datetime

from django.db import models
from django.contrib.auth.models import User

'''
class TeacherBackend(ModelBackend):
    def authenticate(self, request, code=None, **kwargs):
        try:
            teacher = Teacher.objects.get(code=code)
        except Teacher.DoesNotExist:
            return None

        return teacher if self.user_can_authenticate(teacher) else None

    def get_user(self, user_id):
        try:
            return Teacher.objects.get(pk=user_id)
        except Teacher.DoesNotExist:
            return None
'''
# Create your models here.

'''
class Teacher(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


    def is_authenticated(self):
        return True  # Always returns True for user objects

    def __str__(self):
        return self.code
'''
class Subject(models.Model):
    subject = models.CharField(max_length=50)

    def __str__(self):
        return self.subject


class Grade(models.Model):
    grade = models.SmallIntegerField()

    def __str__(self):
        return str(self.grade)

class ClassUnit(models.Model):
    description = models.TextField(null=True, blank=True, default='Key 7 or class 9E')
    created = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    #teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject.subject + ' ' + self.teacher.code + ' ' + str(self.grade)


class Learner(models.Model):
    name = models.CharField(max_length=150)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class LearnerClass(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    classunit = models.ForeignKey(ClassUnit, on_delete=models.SET_NULL, null=True)
    learner = models.ForeignKey(Learner, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.classunit.subject.subject + ' ' + self.learner.name + ' | '  + \
              self.created.strftime('%d-%m-%Y')


    


