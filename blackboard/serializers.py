from rest_framework import serializers
from django.http import JsonResponse
from .models import DATASET_NLP, DATASET_ANSWER
import json

class DatasetNLPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DATASET_NLP
        fields = ('conversation_id', 'question', 'question_intent', 'question_ner')
        # queryset = DATASET_NLP.objects.filter(filteras = "id").values()
        read_only_field = ('conversation_id')
        # return JsonResponse({"models_to_return": list(queryset)})


class DatasetAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DATASET_ANSWER
        fields = ('conversation_id', 'answer', 'answer_intent', 'answer_ner', 'quest_ner')
        read_only_field = ('conversation_id')