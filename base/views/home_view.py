from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from base.models import ClassUnit


@login_required(login_url='index')
def home(request):
    #Get current user and classes
    current_user = request.user
    classes = ClassUnit.objects.filter(user=current_user).order_by('subject')

    ##############################################################
    # Redirect to manage_absentees
    if request.method == 'POST' and request.POST.get('btnAbsentees'):
        return redirect('manage_absentees')
    
    ##############################################################
    #Redirect to manage_classes
    if request.method == 'POST' and request.POST.get('btnClasses'):
        return redirect('manage_classes')
    
    ##############################################################
    #Redirect to manage_stats
    if request.method == 'POST' and request.POST.get('btnStats'):
        return redirect('manage_stats')
    
    ##############################################################


    #Define the output context
    context = {'classes' : classes, 'current_user' : current_user}

    return render(request,'base/home.html', context)
    