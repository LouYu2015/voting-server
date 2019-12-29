from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Question
from .serializers import QuestionSerializer


@csrf_exempt
@api_view(["GET"])
def question_list_view(request, format=None):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)