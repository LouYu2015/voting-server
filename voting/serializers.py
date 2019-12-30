from rest_framework import serializers
from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "message"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "enable", "message", "min_num_chosen", "max_num_chosen", "choices"]


class ChoiceCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Choice
        fields = ["id", "message", "count"]

