from django.urls import path
from . import views

#Url Config
urlpatterns = [
    path('hello/',views.say_hello)
]
