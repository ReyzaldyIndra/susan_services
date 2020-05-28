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
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "id_ID")


db = mysql.connector.connect(
    host="susan-db.cpfkct9edcfy.us-east-1.rds.amazonaws.com",
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
        cursor_answer = db.cursor()
        cursor_date = db.cursor()
        cursor_other = db.cursor()
    
        post_data = request.data
        sentence = post_data['sentence']
        print(sentence)
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
        'B-POLIKLINIK_RUJUKAN','I-POLIKLINIK_RUJUKAN', 'I-KELAS_RAWAT']
        str_ner = Filter(ans_ner, substr)
        join_str = "".join(str_ner)
        print(join_str)
        if (join_str != "") :
            q_id = "SELECT id_answer FROM tbl_answer WHERE ner='"+join_str+"' AND intent='"+ans+"';"
            cursor_answer.execute(q_id)
            res_ans_id = cursor_answer.fetchone()
            db.commit()
            try:
                for p in res_ans_id:
                    answer_id = p
                    print(answer_id, 'answer_id')
            except Exception as e:
                q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='OTHERS';"
                print("kosong cuk")
                cursor.execute(q_ans)
                results = cursor.fetchall()
                for data in results:
                    string_ans = ','.join(data).replace(',', ' ')
                return Response({
                    'answer': string_ans,
                    'intent': ans
                    })

        elif (join_str == "") :
            # q_ans = ""
            print(ans)
            if (ans == 'CLOSINGS'):
                q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='CLOSINGS';"
                # q_ans = "SELECT tbl_answer.jawaban, tbl_record.jenis_kunjungan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
                
            elif (ans == 'GREETINGS'):
                q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='GREETINGS';"
                # q_ans = "SELECT tbl_answer.jawaban, tbl_record.jenis_kunjungan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
        
            elif (ans == 'OTHERS'):
                q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='OTHERS';"
        
        if (ans == "TRANSACTION"):
            if (answer_id == 1) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_transaction_biaya.kelas_rawat_biaya FROM tbl_answer JOIN tbl_transaction_biaya JOIN tbl_user ON tbl_user.id_transaction_biaya=tbl_transaction_biaya.id_transaction_biaya WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line = '"+ userLineId+"' AND tbl_answer.id_answer = 1;"
                q_ans_add = "SELECT tbl_answer.jawaban, tbl_transaction_biaya.biaya_kelas_biaya FROM tbl_answer JOIN tbl_transaction_biaya JOIN tbl_user ON tbl_user.id_transaction_biaya=tbl_transaction_biaya.id_transaction_biaya WHERE tbl_answer.ner='' AND tbl_user.id_user_line = '"+ userLineId+"' AND tbl_answer.id_answer = 31;"
                cursor.execute(q_ans)
                
                ans_kelas = cursor.fetchall()
                
                db.commit()

                for data_kelas in ans_kelas:
                    string_ans_kelas = data_kelas
                    answer_kelas = ','.join(data_kelas).replace(',', ' ')
                    print(answer_kelas, 'strkelas')
                    cursor_other.execute(q_ans_add)
                    ans_biaya = cursor_other.fetchall()
                    db.commit()
                    
                    for data_biaya in ans_biaya:
                        print(data_biaya, 'databiaya')
                        string_ans_biaya = data_biaya
                        answer_biaya = ','.join(data_biaya).replace(',', ' ')
                        print(answer_biaya, 'strbiaya')

                        return Response({
                            'answer': answer_kelas + " dengan biaya " + answer_biaya,
                            'intent': ans
                        })
            elif (answer_id == 24) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_transaction_tagihan.biaya_kelas_tagihan FROM tbl_answer JOIN tbl_transaction_tagihan JOIN tbl_user ON tbl_user.id_transaction_tagihan=tbl_transaction_tagihan.id_transaction_tagihan WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line = '"+userLineId+"' AND tbl_answer.id_answer = 24;"
            elif (answer_id == 30) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_transaction_iuran.kelas_rawat_iuran FROM tbl_answer JOIN tbl_transaction_iuran JOIN tbl_user ON tbl_user.id_transaction_iuran=tbl_transaction_iuran.id_transaction_iuran WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line='"+userLineId+"' AND tbl_answer.id_answer = 30;"
                q_ans_add = "SELECT tbl_answer.jawaban, tbl_transaction_iuran.biaya_kelas_iuran FROM tbl_answer JOIN tbl_transaction_iuran JOIN tbl_user ON tbl_user.id_transaction_iuran=tbl_transaction_iuran.id_transaction_iuran WHERE tbl_answer.ner='' AND tbl_user.id_user_line = '"+userLineId+"' AND tbl_answer.id_answer = 31;"
                cursor.execute(q_ans)
                
                ans_kelas = cursor.fetchall()
                
                db.commit()

                for data_kelas in ans_kelas:
                    string_ans_kelas = data_kelas
                    answer_kelas = ','.join(data_kelas).replace(',', ' ')
                    print(answer_kelas, 'strkelas')
                    cursor_other.execute(q_ans_add)
                    ans_biaya = cursor_other.fetchall()
                    db.commit()
                    
                    for data_biaya in ans_biaya:
                        print(data_biaya, 'databiaya')
                        string_ans_biaya = data_biaya
                        answer_biaya = ','.join(data_biaya).replace(',', ' ')
                        print(answer_biaya, 'strbiaya')

                        return Response({
                            'answer': answer_kelas + ' ' + answer_biaya,
                            'intent': ans
                        })
        elif (ans == "OTHERS"):
                q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='OTHERS';"
        elif (ans == "PROFIL"):
            if (answer_id == 2) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 3) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kabupaten_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 4) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kecamatan_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 5) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kelurahan_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 6 or answer_id == 7) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kepemilikan_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 8) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.jenis_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 9) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 10) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kabupaten_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 11) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.tipe_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 28) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 32) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 33) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kelurahan_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 34) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kecamatan_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 35) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kabupaten_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 36) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.provinsi_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 37) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kabupaten_faskes FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            # elif (answer_id == 12) :
            #     q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kelas_rawat FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
        elif (ans == 'RECORD'):
            if (answer_id == 12) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_profil.kelas_rawat FROM tbl_answer JOIN tbl_profil JOIN tbl_user ON tbl_user.id_profil=tbl_profil.id_profil WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 19):
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.tgl_datang FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
                cursor.execute(q_ans)
                pulang_res = cursor.fetchall()
                db.commit()

                for data in pulang_res:
                    print(data[1])
                    date_datang = data[1]
                    date_str = date_datang.strftime("%d %B %Y")
                    print(date_str, 'hari nya')
                    string_ans = data[0] + ' ' + date_str
                    print(string_ans, 'jawaban+hari')
                    return Response({
                        'answer': string_ans,
                        'intent': ans
                    })
            elif (answer_id == 20) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.tgl_pulang FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
                cursor.execute(q_ans)
                pulang_res = cursor.fetchall()
                db.commit()

                for data in pulang_res:
                    print(data[1])
                    date_pulang = data[1]
                    date_str = date_pulang.strftime("%d %B %Y")
                    print(date_str, 'hari nya')
                    string_ans = data[0] + ' ' + date_str
                    print(string_ans, 'jawaban+hari')
                    return Response({
                        'answer': string_ans,
                        'intent': ans
                    })
            elif (answer_id == 21) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.tgl_tindakan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
                cursor.execute(q_ans)
                tindakan_res = cursor.fetchall()
                db.commit()

                for data in tindakan_res:
                    print(data[1])
                    date_tindakan = data[1]
                    date_str = date_tindakan.strftime("%d %B %Y")
                    print(date_str, 'hari nya')
                    string_ans = data[0] + ' ' + date_str
                    print(string_ans, 'jawaban+hari')
                    return Response({
                        'answer': string_ans,
                        'intent': ans
                    })
            elif (answer_id == 22) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.poliklinik_rujukan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 13) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.segmen FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 14) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.disease FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 15) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.status_pulang FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
                if (ans != 'RECORD'):
                    q_ans = "SELECT jawaban FROM tbl_answer WHERE intent='OTHERS';"
            elif (answer_id == 16) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.hospital FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 17) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.tingkat_layanan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 18) :
                q_ans = "SELECT tbl_answer.jawaban, tbl_record.jenis_kunjungan FROM tbl_answer JOIN tbl_record JOIN tbl_user ON tbl_user.id_profil=tbl_record.id_record WHERE tbl_answer.ner='"+join_str+"' AND tbl_user.id_user_line ='"+userLineId+"'"
            elif (answer_id == 29) :
                q_ans = "SELECT tbl_answer.jawaban FROM tbl_answer WHERE tbl_answer.ner='"+join_str+"'"

       
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
        str_ktp = ""
        str_id_line = ""
        cursor = db.cursor()
        cursor_ktp = db.cursor()
        userLineId = request.data['userLineId']
        no_ktp = request.data['ktp']
        q_put = "UPDATE tbl_user SET id_user_line='"+userLineId+"' WHERE no_ktp='"+no_ktp+"';"
        cursor.execute(q_put)
        db.commit()
        
        q_ktp = "SELECT no_ktp, id_user_line FROM tbl_user WHERE no_ktp="+no_ktp+" OR id_user_line='"+userLineId+"';"
        try:
            print(q_ktp)
            cursor_ktp.execute(q_ktp)
            result_ktp = cursor_ktp.fetchall()
            print(cursor_ktp.rowcount, "record(s) affected")
            db.commit()
            if (cursor.rowcount == -1):
                print("No KTP data")
                str_id_line = ""
                str_ktp = ""
            elif (cursor.rowcount >= 1):
                for data in result_ktp:
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
