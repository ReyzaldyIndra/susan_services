from django.shortcuts import render
from django.http import HttpResponse
# from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DatasetNLPSerializer, DatasetAnswerSerializer
from .models import DATASET_NLP, DATASET_ANSWER
from django.http import JsonResponse
import requests

class NLPViewSet(viewsets.ModelViewSet):
    queryset = DATASET_NLP.objects.all().order_by('id')
    serializer_class = DatasetNLPSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = DATASET_ANSWER.objects.all().order_by('id')
    serializer_class = DatasetAnswerSerializer

class ListenerAPI(APIView):
    def post(self, request):
        #baca data post request
        post_data = request.data
        sentence = post_data['sentence']
        
        respon = requests.get('http://111.223.254.14/nlp/?sentence_intent='+ sentence)
        respon_ner = requests.get('http://111.223.254.14/ner/?sentence=berapa%20biaya%20bpjs%20saya?')
        response_data = respon.json()
        response_data_ner = respon_ner.json()
        ans = response_data['ans']
        ans_ner = response_data_ner['ner']

        #proses masukin sini
        #ambil record di DB berdasarkan hasil proses
        
        string_ner = ''.join(ans_ner)
        # print(string_ner)
            
        answer = DATASET_ANSWER.objects.filter(answer_intent=ans).get(question_ner=string_ner)
        # print(ans_ner)

        # response
        return Response({
            'answer': answer.answer 
        })
