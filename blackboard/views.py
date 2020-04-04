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
        respon_ner = requests.get('http://111.223.254.14:5001/?sentence_ner='+ sentence)
        response_data = respon.json()
        response_data_ner = respon_ner.json()
        ans = response_data['ans']
        ans_ner = response_data_ner['ner']

        substr = ['B-PROVINSI_FASKES', 'B-FIN', 'B-KABUPATEN_FASKES', 'B-KECAMATAN_FASKES', 'B-KELURAHAN_FASKES',
        'B-KEPEMILIKAN_FASKES','B-ORG','I-KEPEMILIKAN_FASKES', 'B-JENIS_FASKES','I-JENIS_FASKES', 'I-PROVINSI_FASKES',
        'I-KABUPATEN_FASKES', 'B-TIPE_FASKES','I-TIPE_FASKES', 'B-KELAS_RAWAT', 'B-SEGMEN',
        'B-DISEASE', 'B-STATUS_PULANG','B-HOSPITAL','I-HOSPITAL', 'B-TINGKAT_LAYANAN','I-TINGKAT_LAYANAN', 
        'B-JENIS_KUNJUNGAN','I-JENIS_KUNJUNGAN','B-TGL_DATANG', 'B-TGL_PULANG', 'B-TGL_TINDAKAN','I-TGL_TINDAKAN',
        'B-POLIKLINIK_RUJUKAN','I-POLIKLINIK_RUJUKAN']
        str_ner = Filter(ans_ner, substr)
        join_str = "".join(str_ner)
        print(join_str)
                    # print(ans)
        if (ans == "TRANSACTION"):
            q_ans = "SELECT tbl_answer.jawaban, tbl_transaction_biaya.biaya_kelas_biaya FROM tbl_answer JOIN tbl_transaction_biaya JOIN tbl_user  ON tbl_user.id_transaction_biaya=tbl_transaction_biaya.id_transaction_biaya WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+ userLineId+"'"                
        elif (ans == "PROFIL"):
            q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
        elif (ans == 'RECORD'):
            q_ans = "SELECT tbl_answer.jawaban, tbl_record.segmen FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
        elif (ans == 'CLOSINGS'):
            q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='CLOSINGS';"
        elif (ans == 'GREETINGS'):
            q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='GREETINGS';"
        
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
        cursor_ktp =  db.cursor()
        message = ""
        str_ktp = ""
        userLineId = request.data['userLineId']
        no_ktp = request.data['ktp']
        q_register = "INSERT INTO tbl_user (no_ktp, nama, id_user_line, id_profil, id_record, id_transaction_biaya, id_transaction_iuran, id_transaction_tagihan, id_answer) VALUES ("+ no_ktp+", 'NULL', '" + userLineId + "', 1, 1, 1, 1, 1, NULL);"
        cursor.execute(q_register)
        db.commit()
        if mysql.connector.errors.IntegrityError:
                message = "duplicate entry no_ktp"
                str_ktp = ""
        elif mysql.connector.errors.InternalError:
                message = "Database exception"
                str_ktp = ""
        elif mysql.connector.DatabaseError:
                message = "Timeout or db error"
                str_ktp = ""
        elif mysql.connector.errors.IntegrityError:
                message = "duplicate entry no_ktp"
                str_ktp = ""
        # print(q_register)
        print(cursor.rowcount, "record(s) found")
        if (cursor.rowcount == -1):
            message = "Can't write KTP"
            str_ktp = ""
        elif (cursor.rowcount >= 1):
            message = "Successfully registered data"
            q_ktp = "SELECT no_ktp FROM tbl_user WHERE id_user_line='" + userLineId + "';"
            cursor_ktp.execute(q_ktp)
            result = cursor_ktp.fetchone()
            db.commit()
            for data in result:
                str_ktp = data
            
            
        return Response({
            'message': message,
            'ktp': str_ktp
        })

def Filter(string, substr): 
    return [str for str in string  
    if re.match(r'[^\d]+|^', str).group(0) in substr] 
