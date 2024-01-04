from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import datetime

from base.models import ClassUnit, Learner, LearnerClass


@login_required(login_url='index')
def submit_absentees(request, classpk):

    #Extract all absentees from model LearnerClass that match today's date.
    absentees = LearnerClass.objects.filter(classunit=classpk, created__date=datetime.date.today())
    obj_class = ClassUnit.objects.get(id=classpk)


    #Current User
    current_user = request.user

    #Fetch a list of all learners 
    #We shouldn't need this anymore - pending delete
    #learners = Learner.objects.all()

    if request.method == 'POST':

        #btnAddAbsentee
        if request.POST.get('btnAddAbsentee'):

        #Capture user input
            learner_id = request.POST.get('absentStudentsInputId')
             
            
            try:
                #fetch Learner object
                learner = Learner.objects.get(id=learner_id)
            except Learner.DoesNotExist:
                learner = None
                messages.error = (request, 'Learner not found, please try again.')

            #Add learner to LearnerClass
            if learner:
                try:
                    new_absentee= LearnerClass(learner=learner, classunit=obj_class)
                    new_absentee.save()
                    messages.success(request, 'Learner successfully added')
                except Exception as e:
                    messages.error(request, 'Error: ' + str(e))


            #btnAddAbsenteeContext
            context = {'current_user' : current_user, 'absentees' : absentees}
            return render (request, 'base/submit_absentees.html', context)
        

        '''
        if request.POST.get('selected_learner'):

            #fetch learner from db
            try:
                del_learner = request.POST.get('selected_learner')
                del_learner = Learner.objects.get(name=del_learner)
            except Learner.DoesNotExist:
                del_learner = None
                messages.error = (request, 'Learner cannot be deleted, please contact admin.')
            
            #Remove learner from list of selected learners
            selected_learners.remove(del_learner.name)
            selected_ids.remove(del_learner.id)

            #Update session
            request.session['selected_learners'] = selected_learners   
            request.session['selected_ids'] = selected_ids

            #Del learner context
            context = {'current_user' : current_user, 'learners' : learners, 'selected_learners' : selected_learners}
            return render(request, 'base/submit_absentees.html', context)
            '''        
       
    #Context
    context = {'current_user' : current_user, 'absentees' : absentees}

    return render (request, 'base/submit_absentees.html', context)

##############################################################################
def autocomplete(request):
    query = request.GET.get('term', '')
    learners = Learner.objects.filter(name__icontains=query)[:10]  # Adjust the number of suggestions as needed
    suggestions = [{'label':f"{learner.name} | Gr {learner.grade}", 'value': learner.id} for learner in learners]
    return JsonResponse(suggestions, safe=False)

##############################################################################
def deleteitem(request):
    learner_name = request.POST.get('learnerName')
    learner_id = request.POST.get('learnerId')
    print(learner_id)
    try:
        del_learner = LearnerClass.objects.get(id=learner_id)
        print(del_learner.learner_id)
    except Learner.DoesNotExist:
        del_learner = None
        return JsonResponse({'message': 'Learner not found'}, status=404)

    
    try:
        del_learner.delete()
        print('deleted')
        return JsonResponse({'message': 'Learner deleted successfully'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    #return JsonResponse({'status': 'success'}, status=200)
