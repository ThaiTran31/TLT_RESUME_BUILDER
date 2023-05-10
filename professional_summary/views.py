from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .generator.gramformer import GrammarCorrect
from .generator.gpt2_generator import GPT2Generator
from django.conf import settings

generator = GPT2Generator() if settings.ENABLE_GPT2 else None
grammar_correct = GrammarCorrect() if settings.ENABLE_GRAMFORMER else None

class Suggestions(APIView):
    def post(self, request, format=None):
        if generator == None or grammar_correct == None:
            return Response(data={'details': "Not available"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requestId = request.data['requestId']
            sequences = request.data['sequences']
            sequences = ''.join(sequences)
            generated_sequences = sequences
            if settings.ENABLE_GPT2:
                generated_sequences = generator.generate_sequences(sequences)
            if  settings.ENABLE_GPT2 and settings.ENABLE_GRAMFORMER:
                generated_sequences = grammar_correct.correct(generated_sequences)
            return Response(data={'data': generated_sequences, 'responseId': requestId}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
