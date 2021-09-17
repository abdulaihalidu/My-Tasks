from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView as UserLogout

urlpatterns = [
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(next_page='login'), name="logout"),
    path('sign-up/', UserSignUP.as_view(), name="sign-up"),
    path('', TaskList.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskDetails.as_view(), name="task-details"),
    path('create-task/', CreateTask.as_view(), name="create-task"),
    path('update-task/<int:pk>/', UpdateTask.as_view(), name="update-task"),
    path('delete-task/<int:pk>/', DeleteTask.as_view(), name="delete-task"),
    path('task-completed/<int:pk>/', mark_as_done, name="task-completed"),

]
