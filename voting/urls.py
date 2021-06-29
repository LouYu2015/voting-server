from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import question_list_view, vote_count_view, update_vote_view, get_selected_view, \
    enable_serial_number, disable_serial_number

urlpatterns = [
    path('questions/', question_list_view),  # Get a list of questions
    path('vote_count/<int:id>/', vote_count_view),  # Get vote count for a question
    path('update_vote/<int:question_id>/', update_vote_view),  # Update a user's vote for a question
    path('get_selected/<str:serial_number>/', get_selected_view),  # Get the choice selected by the user
    path('enable/', enable_serial_number),  # Enable questions
    path('disable/', disable_serial_number)  # Disable questions
]

urlpatterns = format_suffix_patterns(urlpatterns)
