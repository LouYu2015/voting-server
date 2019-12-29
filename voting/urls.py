from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import question_list_view, vote_count_view

urlpatterns = [
    path('questions/', question_list_view),
    path('vote_count/<int:id>/', vote_count_view)
]

urlpatterns = format_suffix_patterns(urlpatterns)
