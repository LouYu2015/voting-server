from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceCountSerializer
from django.db.models import Count


@api_view(["GET"])
def question_list_view(request, format=None):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def vote_count_view(request, id: int, format=None):
    if request.method == "GET":
        choices = Choice.objects.filter(question__id=id).annotate(count=Count('vote'))
        serializer = ChoiceCountSerializer(choices, many=True)
        return Response(serializer.data)

