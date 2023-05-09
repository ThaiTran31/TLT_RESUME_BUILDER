from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import ComplexSection, EmploymentHistory, Education, Skill, Link, Custom
from .serializers import ComplexSectionSerializer, EmploymentHistorySerializer, EducationSerializer, SkillSerializer, LinkSerializer, CustomSerializer


class ComplexSectionDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ComplexSection.objects.all()
    serializer_class = ComplexSectionSerializer


class EmploymentHistoryDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EmploymentHistory.objects.all()
    serializer_class = EmploymentHistorySerializer


class EducationDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class SkillDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class LinkDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class CustomDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer


class ComplexSectionDetail(generics.RetrieveAPIView):
    queryset = ComplexSection.objects.all()
    serializer_class = ComplexSectionSerializer


class ComplexSectionUpdate(generics.UpdateAPIView):
    queryset = ComplexSection.objects.all()
    serializer_class = ComplexSectionSerializer


class ComplexSectionCreate(APIView):
    def post(self, request, format=None):
        # print("------------------------------------------")
        # print(request.data)
        # print("------------------------------------------")
        complex_section_serializer = ComplexSectionSerializer(data=request.data)
        if complex_section_serializer.is_valid():
            # print("------------------------------------------")
            # print(complex_section_serializer.validated_data)
            # print("------------------------------------------")
            complex_section_instance = complex_section_serializer.save()
            # print(complex_section_serializer.data)
            # print(complex_section_instance)
            section_type = request.data.get("section_type")
            items = request.data.get(section_type)
            if section_type == "employment_histories":
                for item in items:
                    id = item.get("id", None)
                    if id is None:
                        serializer = EmploymentHistorySerializer(data=item)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save(complex_section=complex_section_instance)  # return an instance
                    else:
                        try:
                            instance = EmploymentHistory.objects.get(id=id)
                        except EmploymentHistory.DoesNotExist:
                            raise Http404
                        serializer = EmploymentHistorySerializer(instance, data=item)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
            elif section_type == "educations":
                pass
            elif section_type == "skills":
                pass
            elif section_type == "links":
                pass
            else:  # section_type == "customs"
                pass
            return Response(complex_section_serializer.data, status=status.HTTP_201_CREATED)
        return Response(complex_section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
