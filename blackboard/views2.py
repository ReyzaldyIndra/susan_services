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

class ListenKTPAPI(APIView):
    def get(self, request):
        str_ktp = ""
        cursor = db.cursor()
        userLineID = request.data['userLineId']
        q_ktp = "SELECT no_ktp FROM tbl_user WHERE id_user_line='" + userLineID + "';"
        cursor.execute(q_ktp)
        try:
            result = cursor.fetchone()
            print(cursor.rowcount, "record(s) affected")
            if (cursor.rowcount == -1):
                print("No KTP data")
            elif (cursor.rowcount >= 1):
                for data in result:
                    str_ktp = data
        except mysql.connector.errors.InternalError as err:
            print("Database exception", err)
        
        return Response({
            'userLineId': userLineID,
            'ktp': str_ktp
        })