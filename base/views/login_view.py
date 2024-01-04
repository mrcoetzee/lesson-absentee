from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    
    if request.method == 'POST':
        #Get teacher code input
        teacherCode = request.POST.get('teacher_code')
        registerCode = request.POST.get('register_code')

        if request.POST.get('btnLogin'):
            #Check if teacher code exists
            
            try:
                teacher = User.objects.get(username=teacherCode)
            except User.DoesNotExist:
                messages.error(request, "Teacher code does not exist")
                teacher = None

            
            if teacher is not None:
                login(request, teacher)
                return redirect('home')
            
            
                
        #Create new teacher code   
        if request.POST.get('btnRegister') and registerCode is not None:
            
            try:
                new_user = User.objects.create_user(username=registerCode)
            except Exception as e:
                messages.error(request, "User already exists, logged in with that code")

            user = User.objects.get(username=registerCode)
            if user is not None:
                login(request, user)
                return redirect('home')
            
    return render(request,'base/login.html')
    

##############################################################################

def logout_user(request):
    logout(request)
    return redirect('index')

'''
def index(request):

    if request.method == 'POST':
        #Get teacher code input
        teacherCode = request.POST.get('teacher_code')

        new_user = User.objects.create_user(username=teacherCode)

    return render(request,'base/login.html')
    '''