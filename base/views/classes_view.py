from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from base.models import ClassUnit, Subject, Grade


# Create your views here.
@login_required(login_url='index')
def manage_classes(request):
    
    current_user = request.user
    classes = ClassUnit.objects.filter(user=current_user).order_by('subject')
    
    if request.method == 'POST':
        
        #Capture selected class
        class_id = request.POST.get('classid')
        
        if (class_id) and (request.POST.get('btnDelete')):
            class_delete = ClassUnit.objects.get(id=class_id)
            class_delete.delete()
            return redirect('manage_classes')
        
        if request.POST.get('btnAdd'):
            return redirect('add_class')

    context = {'classes' : classes, 'current_user' : current_user}
    return render(request, 'base/manage_classes.html', context)


@login_required(login_url='index')
def add_class(request):

    current_user = request.user
    classes = ClassUnit.objects.filter(user=current_user)

    #Fetch a list of subjects
    subjectList = Subject.objects.all()

    #Fetch a list of grades
    gradeList = Grade.objects.all()

    context = {'classes' : classes, 'current_user' : current_user, 'subjectList' : subjectList, \
               'gradeList' : gradeList}
    
    if request.method == 'POST':
        new_class = ClassUnit(description=request.POST.get('description'), \
                              subject=Subject.objects.get(subject=request.POST.get('subject')), \
                             grade=Grade.objects.get(grade=request.POST.get('grade')), \
                                user=current_user)
        new_class.save()
        return redirect('manage_classes')


    return render(request, 'base/add_class.html', context)