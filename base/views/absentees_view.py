from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import datetime

from base.models import ClassUnit, Learner, LearnerClass


@login_required(login_url='index')
def manage_absentees(request):
    #Current User
    current_user = request.user

    #Get classes for current user
    classes = ClassUnit.objects.filter(user=current_user).order_by('subject')


    #Process inputs
    if request.method == 'POST':
        #Get selected class
        try:
            selected_class = request.POST.get('classid')
            selected_class = ClassUnit.objects.get(id=selected_class)
        except ClassUnit.DoesNotExist:
            selected_class = None
            messages.error(request, 'Please select a class')


        #btnSubmitAbsentees
        if request.POST.get('btnSubmitAbsentees') and selected_class:
            classpk = selected_class.id
            return redirect('submit_absentees', classpk=classpk)
        elif not selected_class:
            messages.error(request, 'Please select a class')

        #btnManageAbsentees
        if request.POST.get('btnManageAbsentees') and selected_class:
            classpk = selected_class.id
            return redirect('view_absentees', classpk=classpk)

    #Context
    context = {'current_user' : current_user, 'classes' : classes}

    return render (request, 'base/manage_absentees.html', context)

##############################################################################


@login_required(login_url='index')
def view_absentees(request, classpk):

    #Current User
    current_user = request.user

    #Context
    context = {'current_user' : current_user}

    return render(request, 'base/view_absentees.html', context)