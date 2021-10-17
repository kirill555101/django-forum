from django.urls import path

from main.views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('hot/', hot, name='hot'),
    path('ask/', ask, name='ask'),
    path('question/<int:id>/', question, name='question'),
    path('question/<int:id>/answer/new/', answer, name='answer'),
    path('tag/<int:id>/', tag, name='tag'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
]
