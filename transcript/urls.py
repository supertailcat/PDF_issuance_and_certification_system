from django.urls import path
from . import views
# from .views import SignView

urlpatterns = [
    path('sign/', views.sign),
    # path('new/', SignView.as_view()),
    path('validate/', views.validate)
]