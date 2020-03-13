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
        cursor_ktp = db.cursor()
        cursor_user = db.cursor()

    
        post_data = request.data
        sentence = post_data['sentence']
        userLineId = post_data['userLineId']

        # Berapa biaya BPJS untuk kelas 1?
        respon = requests.get('http://111.223.254.14:5000/?sentence_intent='+ sentence)
        # respon_ner = requests.get('http://111.223.254.14:5001/?sentence_ner=' + sentence, verify=False, timeout=100)
        response_data = respon.json()
        # response_data_ner = respon_ner.json()
        ans = response_data['ans']
        # ans_ner = response_data_ner['ner']
                    # print(ans)
        if (ans == "TRANSACTION"):
            q_ans = "SELECT tbl_answer.jawaban, tbl_transaction_biaya.biaya_kelas_biaya FROM tbl_answer JOIN tbl_transaction_biaya JOIN tbl_user  ON tbl_user.id_transaction_biaya=tbl_transaction_biaya.id_transaction_biaya WHERE tbl_answer.ner='B-FIN' AND tbl_user.no_ktp ="+ id_data[1]+" AND tbl_answer.id_answer = 25;"                
        elif (ans == "PROFIL"):
            q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='B-PROVINSI_FASKES' AND tbl_user.no_ktp ="+id_data[1]+" AND tbl_answer.id_answer = 2;"
        elif (ans == 'RECORD'):
            q_ans = "SELECT tbl_answer.jawaban, tbl_record.segmen FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='B-SEGMEN' AND tbl_user.no_ktp ="+id_data[1]+" AND tbl_answer.id_answer = 13;"
        elif (ans == 'CLOSINGS'):
            q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='CLOSINGS';"
        
        print(q_ans)
        cursor.execute(q_ans)
        results = cursor.fetchall()

        for data in results:
            string_ans = ','.join(data).replace(',', ' ')
  

        return Response({
            'answer': string_ans,
            'intent': ans
            # 'ner': ans_ner
        })

class ListenKTPAPI(APIView):
    def get(self, request):
        cursor = db.cursor()
        userLineID = request.data['userLineId']
        q_ktp = "SELECT tbl_user.no_ktp FROM tbl_user WHERE id_user_line='" + userLineID + "';"
        cursor.execute(q_ktp)
        result = cursor.fetchone()
        for data in result:
            str_ktp = data
        return Response({
            'userLineId': userLineID,
            'ktp': str_ktp
        })

class UpdateKTPApi(APIView):
    def put(self, request):
        cursor = db.cursor()
        cursor_ktp = db.cursor()
        
        # first_name = request.data['first_name']
        userLineId = request.data['userLineId']
        no_ktp = request.data['ktp']
        
        q_put = "UPDATE tbl_user SET no_ktp='"+no_ktp+"' WHERE id_user_line='"+userLineId+"';"
        q_ktp = "SELECT tbl_user.no_ktp FROM tbl_user WHERE id_user_line='" + userLineId + "';"
        cursor.execute(q_put)
        db.commit()
        print(cursor.rowcount, "record(s) affected")
        cursor_ktp.execute(q_ktp)
        result_ktp = cursor_ktp.fetchone()
        print(userLineId)
        print(no_ktp)
        for data in result_ktp:
            print("ktp result", data)
        return Response({
            'userLineId': userLineId,
            'ktp': data
        })
        # kelas_rawat = request.data['kelas_rawat']
        # q_register = "INSERT INTO tbl_user (no_ktp, nama, id_user_line, id_profil, id_record, id_transaction_biaya, id_transaction_iuran, id_transaction_tagihan, id_answer) VALUES (" + no_ktp + first_name + userLineId + albert94, +kelas_rawat 1, 1, 1, 1, 1, NULL);"

class PostKTPApi(APIView):
    def post(self, request):
        cursor = db.cursor()
        userLineId = request.data['userLineId']
        no_ktp = request.data['ktp']
        # name = request.data['name']
        q_register = "INSERT INTO tbl_user (no_ktp, nama, id_user_line, id_profil, id_record, id_transaction_biaya, id_transaction_iuran, id_transaction_tagihan, id_answer) VALUES ("+ no_ktp+", 'NULL', '" + userLineId + "', 1, 1, 1, 1, 1, NULL);"
        cursor.execute(q_register)
        db.commit()
        print(cursor.rowcount, "record(s) affected")
        if (cursor.rowcount >= 1):
            message = "Successfully registered user id"
        elif (cursor.rowcount == 0):
            message = "Registration failed"
        
        
        return Response({
            'message': message,
            'userLineId': userLineId,
            "ktp": no_ktp
        })
