from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import question_list_view, vote_count_view, update_vote_view, get_selected_view, \
    enable_serial_number, disable_serial_number

urlpatterns = [
    path('questions/', question_list_view),
    path('vote_count/<int:id>/', vote_count_view),
    path('update_vote/<int:question_id>/', update_vote_view),
    path('get_selected/<str:serial_number>/', get_selected_view),
    path('enable/', enable_serial_number),
    path('disable/', disable_serial_number)
]

urlpatterns = format_suffix_patterns(urlpatterns)
