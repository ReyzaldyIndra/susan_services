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
        result = cursor.fetchone()
        print(cursor.rowcount, "record(s) affected")
        if mysql.connector.errors.InternalError:
            print("No KTP data")
        if (cursor.rowcount == -1):
            print("Database exception")
        elif (cursor.rowcount >= 1):
            for data in result:
                str_ktp = data
        return Response({
            'userLineId': userLineID,
            'ktp': str_ktp
        })