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
import mysql.connector


db = mysql.connector.connect(
    host="susandb.cwn5kclnwgbj.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="Rlatpwjd828",
    database="susan"
)
class NLPViewSet(viewsets.ModelViewSet):
    queryset = DATASET_NLP.objects.all().order_by('id')
    serializer_class = DatasetNLPSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = DATASET_ANSWER.objects.all().order_by('id')
    serializer_class = DatasetAnswerSerializer

class ListenerAPI(APIView):
    def post(self, request):
        cursor = db.cursor()
        q_ans = "SELECT tbl_answer.jawaban, tbl_transaction.biaya_kelas, tbl_user.nama FROM tbl_answer JOIN tbl_transaction JOIN tbl_user  ON tbl_user.id_transaction=tbl_transaction.id_transaction WHERE tbl_answer.ner='B-FIN' AND tbl_user.id_user = 1 AND tbl_answer.id_answer = 1;"
        # q_info = "'SELECT biaya_kelas FROM tbl_transaction WHERE kelas_rawat='Kelas 1'"
        cursor.execute(q_ans)
        results = cursor.fetchall()
        

        for data in results:
            print(data)
            string_ans = ','.join(data).replace(',', ' ')
            print(string_ans)
    
        if db.is_connected():
            print("Successfully connected to the DB")
        #baca data post request
        post_data = request.data
        sentence = post_data['sentence']
        # Berapa biaya BPJS untuk kelas 1?
        respon = requests.get('http://111.223.254.14:5000/?sentence_intent='+ sentence)
        respon_ner = requests.get('http://111.223.254.14:5001/?sentence_ner=' + sentence, verify=False, timeout=100)
        response_data = respon.json()
        response_data_ner = respon_ner.json()
        ans = response_data['ans']
        ans_ner = response_data_ner['ner']
        print(ans)
        print(response_data_ner)

        #proses masukin sini
        #ambil record di DB berdasarkan hasil proses
        
        # string_ner = ','.join(ans_ner)
        # print(string_ner)
        # string_intent = ans
        # answer = DATASET_ANSWER.objects.get(answer_intent=ans)
        # answer = DATASET_ANSWER.objects.get(answer_ner=string_ner).select_related()
        # answer = DATASET_ANSWER.objects.filter(answer_intent=ans).get(answer_ner=string_ner)
        # answer = DATASET_ANSWER.objects.filter(answer_ner=string_ner).select_related()
        # string_answer = ans + ' -> ' + string_ner
        # answer = string_answer
        # print(ans_ner)
        # print(answer)

        # response
        return Response({
            'answer': string_ans
        })