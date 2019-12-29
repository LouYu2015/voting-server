from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import question_list_view

urlpatterns = [
    path('questions/', question_list_view)
]

urlpatterns = format_suffix_patterns(urlpatterns)