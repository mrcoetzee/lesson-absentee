from django.contrib.auth.models import User

new_user = User.objects.create_user(username='RB')
#new_user.save()