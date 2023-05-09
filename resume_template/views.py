from django.http import Http404

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ResumeTemplate
from .serializers import ResumeTemplateSerializer


class ResumeTemplateListAll(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResumeTemplateSerializer

    def get_queryset(self):
        queryset = ResumeTemplate.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class MockResumeTemplate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializers = ResumeTemplateSerializer(data=request.data, many=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
