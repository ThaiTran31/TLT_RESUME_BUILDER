from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .generator import lstm_generator, gpt2_generator, gramformer


class Suggestions(APIView):
    def post(self, request, format=None):
        try:
            requestId = request.data['requestId']
            sequences = request.data['sequences']
            sequences = ''.join(sequences)
            mode = request.data['mode']
            # if (mode == 'tokens'):
            #     return Response(data={'data': lstm_generator.generate_tokens(5, sequences)}, status=status.HTTP_200_OK)
            # elif (mode == 'sequences'):
            #     return Response(data={'data': gramformer.correct(gpt2_generator.generate_sequences(sequences))}, status=status.HTTP_200_OK)
            # else:
            #     return Response(data={'details': "Unsupport mode"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'data': gramformer.correct(gpt2_generator.generate_sequences(sequences)), 'responseId': requestId}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
