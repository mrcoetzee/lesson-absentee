from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('home/',views.home, name="home"),
    path('manage_absentees/', views.manage_absentees, name="manage_absentees"),
    path('submit_absentees/<str:classpk>/', views.submit_absentees, name="submit_absentees"),
    path('view_absentees/<str:classpk>/', views.view_absentees, name="view_absentees"),
    path('manage_classes/', views.manage_classes, name="manage_classes"),
    path('add_class/', views.add_class, name="add_class"),
    path('ajax/autocomplete/', views.autocomplete, name='autocomplete'),
    path('ajax/delete_item/', views.deleteitem, name='deleteitem'),
    

  
    #path('Logout/', views.logoutUser, name='Logout'),
    #path('manageclasses/', views.manageclasses, name="manageclasses"),
   #path('addclass/', views.addClass, name="addclass"),
    #path('absentees/<str:pk>/', views.absentees, name="absentees")
]
