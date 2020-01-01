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
# def index(request):
#     return HttpResponse("Hello. This called the blackboard")

# class GetView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = DATASET_NLP.objects.all()
#     serializer_class = DatasetNLPSerializer

#     def perform_create(self, serializer):
#         serializer.save()

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
        # chat_respon = respon.json()
        # chat_respon = post_data[respon.json()]
        response_data = respon.json()
        ans = response_data['ans']
        
        if ans == 'CLOSINGS':
        #proses masukin sini
            id = 1
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)

        elif ans == 'OTHERS':
        #proses masukin sini
            id = 2
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)

        elif ans == 'RECORD':
        #proses masukin sini
            id = 3
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)

        elif ans == 'PROFIL':
        #proses masukin sini
            id = 4
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)

        elif ans == 'GREETINGS':
        #proses masukin sini
            id = 5
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)

        elif ans == 'TRANSACTION':
        #proses masukin sini
            id = 6
        #ambil record di DB berdasarkan hasil proses
            answer = DATASET_ANSWER.objects.get(id=id)
        
        

        # response
        return Response({
            'answer': answer.answer
            # 'intent': answer.answer_intent  
        })
