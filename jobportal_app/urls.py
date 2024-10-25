
from . import views
from django.urls import path


urlpatterns = [
    path('',views.home, name='home'),
    path('apply/<str:name>/',views.apply, name='apply'),
    path('loginUser/',views.loginUser, name='loginUser'),
    path('register/',views.register, name='register'),
    path('show_vacancy/',views.show_vacancy, name='show_vacancy'),
    path('new_vacancy/<str:name>',views.new_vacancy, name='new_vacancy'),
    path('update_vacancy/<int:vacancy_id>',views.update_vacancy, name='update_vacancy'),
    path('logout/',views.logoutUser, name='logoutUser')
]

