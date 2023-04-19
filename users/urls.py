from django.urls import path
from . import views  


urlpatterns = [

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('account/',views.userAccount, name='account'),
    path('edit-profile/',views.editProfile, name="edit-profile"),

    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name = 'message'),
    path('send-message/<str:pk>/', views.sendMessage, name = 'send-message'),

    path('create/',views.createSkill, name="create-skill"),
    path('update/<str:pk>/',views.updateSkill, name="update-skill"),
    path('delete/<str:pk>/',views.deleteSkill, name="delete-skill"),
    

    path('', views.profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
]