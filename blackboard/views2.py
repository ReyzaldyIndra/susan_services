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
import re

db = mysql.connector.connect(
    host="susan-db.cpfkct9edcfy.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="Rlatpwjd828",
    database="susan"
)

class ListenKTPAPI(APIView):
    def get(self, request):
        str_ktp = ""
        str_id_line = ""
        cursor = db.cursor()
        user_id_line = request.data['userLineId']
        q_ktp = "SELECT no_ktp, id_user_line FROM tbl_user WHERE id_user_line='"+user_id_line+"';"
        cursor.execute(q_ktp)
        try:
            result = cursor.fetchall()
            db.commit()
            print(cursor.rowcount, "record(s) affected")
            if (cursor.rowcount == -1):
                print("No KTP data")
                str_id_line = ""
                str_ktp = ""
            elif (cursor.rowcount >= 1):
                for data in result:
                    str_ktp = data[0]
                    print(data)
                    str_id_line = data[1]
        except Exception as e:
            str_id_line = ""
            str_ktp = ""
        
        return Response({
            'userLineId': str_id_line,
            'ktp': str_ktp
        })

class ListenNERAPI(APIView):
    def post(self, request):
        cursor = db.cursor()
        post_data = request.data
        sentence = post_data['sentence']
        userLineId = post_data['userLineId']
        respon = requests.get('http://111.223.254.14:5001/?sentence_ner='+ sentence)
        response_data = respon.json()
        ans = response_data['ner']
        # fak = [sub.replace('O', '') for sub in ans] 
        # o_remover = fak.replace('O', '')
        # o_split = fak.split()
        substr = ['B-PROVINSI_FASKES', 'B-FIN', 'B-KABUPATEN_FASKES', 'B-KECAMATAN_FASKES', 'B-KELURAHAN_FASKES',
        'B-KEPEMILIKAN_FASKES','B-ORG','I-KEPEMILIKAN_FASKES', 'B-JENIS_FASKES','I-JENIS_FASKES', 'I-PROVINSI_FASKES',
        'I-KABUPATEN_FASKES', 'B-TIPE_FASKES','I-TIPE_FASKES', 'B-KELAS_RAWAT', 'B-SEGMEN',
        'B-DISEASE', 'B-STATUS_PULANG','B-HOSPITAL','I-HOSPITAL', 'B-TINGKAT_LAYANAN','I-TINGKAT_LAYANAN', 
        'B-JENIS_KUNJUNGAN','I-JENIS_KUNJUNGAN','B-TGL_DATANG', 'B-TGL_PULANG', 'B-TGL_TINDAKAN','I-TGL_TINDAKAN',
        'B-POLIKLINIK_RUJUKAN','I-POLIKLINIK_RUJUKAN']
        str_ner = Filter(ans, substr)
        join_str = "".join(str_ner)
        print(join_str)
        return Response({
            'str_ner': str_ner
        })

def Filter(string, substr): 
    return [str for str in string  
    if re.match(r'[^\d]+|^', str).group(0) in substr] 