from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import base64
from ai_bridge.client import ai_agent

class ParseResume(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data['userId']
            file = request.data['file']
            filetype = request.data['fileType']
            parsetype = request.data['parseType']
            filename = userid   
            base64data = base64.b64encode(file.read())
            output = ai_agent.parse_resume(filename, filetype, parsetype, base64data)
            return Response(data=output, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
