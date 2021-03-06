from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Question, Choice, SerialNumber, Vote, JudgeVote
from .serializers import QuestionSerializer, ChoiceCountSerializer
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test


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


@api_view(["GET"])
def judge_vote_count_view(request, id: int, format=None):
    if request.method == "GET":
        choices = Choice.objects.filter(question__id=id).annotate(count=Count('judge_vote'))
        serializer = ChoiceCountSerializer(choices, many=True)
        return Response(serializer.data)


@transaction.atomic
@api_view(["POST"])
def update_vote_view(request, question_id: int, format=None):
    if request.method == "POST":
        try:
            # Get question
            try:
                question = Question.objects.get(id=question_id)
            except ObjectDoesNotExist:
                raise AssertionError("Question doesn't exits")

            if not question.enable:
                raise AssertionError("Question is locked")

            # Assert that input is dictionary
            assert type(request.data) == dict, "Input must be dictionary"

            # Check serial number
            serial_number = request.data["serial_number"]
            assert type(serial_number) == str, "Serial number must be string"
            try:
                serial_number_obj = SerialNumber.objects.get(serial_number=serial_number)
            except ObjectDoesNotExist:
                raise AssertionError("Serial number is not valid")

            if not serial_number_obj.enable:
                raise AssertionError("Serial number valid but not eligible to vote")

            # Check if choices ID are malformated
            choices_ids = request.data["choice_ids"]
            for id in choices_ids:
                assert type(id) == int, "choice ID must be integer"

            # Check if choices are valid
            num_valid_choices = Choice.objects.filter(id__in=choices_ids, question__id=question_id).count()
            assert len(choices_ids) == num_valid_choices, "Some choices are not valid"

            # Check if the number of choices are valid
            assert question.min_num_chosen <= num_valid_choices <= question.max_num_chosen,\
                "The number of choices is not in range [%d, %d]" % (question.min_num_chosen,
                                                                    question.max_num_chosen)

            vote_category = JudgeVote if serial_number_obj.is_judge else Vote
            vote_category.objects.filter(serial_number=serial_number_obj, choice__question__id=question_id).delete()
            for id in choices_ids:
                new_record = vote_category(serial_number=serial_number_obj, choice=Choice.objects.get(id=id))
                new_record.save()
            return Response({"detail": "success"})

        except KeyError as e:
            return Response({"detail": "Malformated input"}, status.HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)


@transaction.atomic
@api_view(["GET"])
def get_selected_view(request, serial_number, format=None):
    if request.method == "GET":
        try:
            # Check serial number
            assert type(serial_number) == str, "Serial number must be string"
            try:
                serial_number_obj = SerialNumber.objects.get(serial_number=serial_number)
            except ObjectDoesNotExist:
                raise AssertionError("Serial number is not valid")

            result = Vote.objects.filter(serial_number__serial_number=serial_number)\
                                 .select_related('choice')
            judge_result = JudgeVote.objects.filter(serial_number__serial_number=serial_number)\
                                    .select_related('choice')
            return Response([{"question": item.choice.question.id,
                              "choice": item.choice.id} for item in result] +
                            [{"question": item.choice.question.id,
                              "choice": item.choice.id} for item in judge_result])
        except AssertionError as e:
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)


def change_serial_number_state(serial_numbers, state):
    for serial_number in serial_numbers:
        try:
            serial_number_obj = SerialNumber.objects.get(serial_number=serial_number)
            serial_number_obj.enable = state
            serial_number_obj.save()
        except ObjectDoesNotExist:
            SerialNumber(serial_number=serial_number, enable=state).save()
    return Response({"detail": "success"})


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
@api_view(["POST"])
def enable_serial_number(request):
    if request.method == "POST":
        return change_serial_number_state(request.data, True)


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
@api_view(["POST"])
def disable_serial_number(request):
    if request.method == "POST":
        return change_serial_number_state(request.data, False)
