from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.student_create),
    path('download/', views.file_download),
    path('verify/', views.verify)
]
