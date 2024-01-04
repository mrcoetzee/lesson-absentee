from django.shortcuts import redirect, render
from .models import Teacher, Subject, Grade, ClassUnit, LearnerClass, Learner
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


######################################################################################################

######################################################################################################

@login_required(login_url='loginpage')
def home(request):

    #Get current user and classes
    current_user = request.user
    classes = ClassUnit.objects.filter(teacher=current_user).order_by('subject')

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

######################################################################################################
def logoutUser(request):
    logout(request)
    return redirect('loginpage')
    

######################################################################################################        
@login_required(login_url='loginpage')
def manageclasses(request):
    
    current_user = request.user
    classes = ClassUnit.objects.filter(teacher=current_user).order_by('subject')
    
    if request.method == 'POST':
        
        class_id = request.POST.get('classid')
        context = {'classes' : classes, 'current_user' : current_user, 'class_id' : class_id}
        
        if (class_id) and (request.POST.get('btnDelete')):
            class_delete = ClassUnit.objects.get(id=class_id)
            class_delete.delete()
            return redirect('manageclasses')
        
        if request.POST.get('btnAdd'):
            return redirect('addclass')
        
        if request.POST.get('btnAbsentees'):
            return redirect('absentees', pk=class_id)
        #return render(request, 'base/absentees.html', context)



    context = {'classes' : classes, 'current_user' : current_user}
    return render(request, 'base/manageclasses.html', context)
############################################################################################################################
@login_required(login_url='loginpage')
def addClass(request):

    current_user = request.user
    classes = ClassUnit.objects.filter(teacher=current_user)

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
                                teacher=current_user)
        new_class.save()
        return redirect('manageclasses')


    return render(request, 'base/addclass.html', context)
############################################################################################################################
@login_required(login_url='loginpage')
def absentees(request, pk):
    #Get the list of selected learners from the session
    selected_learners = request.session.get('selected_learners', [])
    selected_ids = request.session.get('selected_ids', [])

    #Check if the same class has been accessed or reset selected learners
    pk_session = request.session.get('pk', None)
    if pk_session != pk:
        selected_learners = []
        selected_ids = []
        request.session['pk'] = pk

    #Current User
    current_user = request.user

    #Fetch a list of all learners
    learners = Learner.objects.all()
    ##############################################################
    if request.method == 'POST' and request.POST.get('learner'):
        #Collect learner
        learner_id = request.POST.get('learner')

        try:
            #Get learner object
            learner = Learner.objects.get(name=learner_id)

            #Add learner to list of selected learners
            selected_learners.append(learner.name)
            selected_ids.append(learner.id)
            print(f'Learner {selected_learners} and ID: {selected_ids}')  

            # Save the updated list to the session
            request.session['selected_learners'] = selected_learners   
            request.session['selected_ids'] = selected_ids
    
        except Learner.DoesNotExist:
            messages.error(request, 'Learner not found.')

        context = {'current_user' : current_user, 'learners' : learners, \
                   'selected_learners' : selected_learners,\
                   }
        return render(request, 'base/absentees.html', context)
    ##############################################################    
    #Remove learner from list
    if request.method == 'POST' and request.POST.get('selected_learner'):
        #Collect learner
        #print('learner found')
        learner_name = request.POST.get('selected_learner')
        
        try:
            #Get learner object
            learner = Learner.objects.get(name=learner_name)

            #Remove learner from list of selected learners
            selected_learners.remove(learner.name)
            selected_ids.remove(learner.id)

            #Update session
            request.session['selected_learners'] = selected_learners   
            request.session['selected_ids'] = selected_ids
        except:
            messages.error(request, 'Learner was not removed, contact admin.')

        context={'learners' : learners, 'selected_learners' : selected_learners}
        return render(request, 'base/absentees.html', context)
    ##############################################################

    if request.method == 'POST' and request.POST.get('btnSubmit'):
        #Get the class
        class_unit = ClassUnit.objects.get(id=pk)

        #Get the list of learners
        learners_selected = Learner.objects.filter(id__in=selected_ids)
        print('it got in')
        try:
            #Add absentees per learner
            for learner_s in learners_selected:
                new_absentee = LearnerClass(learner=learner_s, classunit=class_unit)
                new_absentee.save()
        except:
            messages.error(request, 'Learner was not added, contact admin.')
        finally:
            #Reset selected learners
            selected_learners = []
            request.session['selected_learners'] = selected_learners
            selected_ids = []
            request.session['selected_ids'] = selected_ids
            return redirect('manageclasses')
        

            




        #Add absentee
        #new_absentee = LearnerClass(learner=learner, class_unit=ClassUnit.objects.get(id=pk))
        #new_absentee.save()

        #return redirect('absentees', pk=pk)


    
    print('yes')

    context = {'current_user' : current_user, 'learners' : learners, 'selected_learners' : selected_learners}

    return render(request, 'base/absentees.html', context)

