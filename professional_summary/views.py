from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ai_bridge.client import ai_agent

class Suggestions(APIView):
    def post(self, request, format=None):
        try:
            requestId = request.data['requestId']
            sequences = request.data['sequences']
            generated_sequences = ai_agent.suggestion_summary(input=sequences)
            return Response(data={'data': generated_sequences, 'responseId': requestId}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
