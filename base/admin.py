from django.contrib import admin
from .models import Subject, Grade, ClassUnit, LearnerClass, Learner

# Register your models here.

#admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(ClassUnit)
admin.site.register(LearnerClass)
admin.site.register(Learner)

