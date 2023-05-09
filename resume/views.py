import copy
from django.http import Http404, HttpResponseBadRequest

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .models import Resume
from .serializers import ResumeSerializer, ResumeListSerializer, ImagesUploadingSerializer
from resume_form.models import PersonalDetails, ProfessionalSummary, ComplexSection, EmploymentHistory, Education, Skill, Link, Custom
from resume_form.serializers import PersonalDetailsSerializer, ProfessionalSummarySerializer, ComplexSectionSerializer, EmploymentHistorySerializer, CustomSerializer, EducationSerializer, LinkSerializer, SkillSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ResumeUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request, format=None):
        try:
            resume_instance = Resume.objects.get(id=request.data.get("id"))
        except Resume.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, resume_instance)
        resume_serializer = ResumeSerializer(resume_instance, data=request.data)
        if resume_serializer.is_valid(raise_exception=True):
            resume_instance = resume_serializer.save()
            # Handling Personal Details
            if request.data.get("personal_details") is not None:
                personal_details = request.data.get("personal_details")
                personal_details_id = personal_details.get("id")
                if personal_details_id is None:
                    personal_details_serializer = PersonalDetailsSerializer(data=personal_details)
                    if personal_details_serializer.is_valid(raise_exception=True):
                        personal_details_serializer.save(resume=resume_instance)
                else:
                    try:
                        personal_details_instance = PersonalDetails.objects.get(id=personal_details_id)
                    except PersonalDetails.DoesNotExist:
                        raise Http404
                    personal_details_serializer = PersonalDetailsSerializer(personal_details_instance, data=personal_details)
                    if personal_details_serializer.is_valid(raise_exception=True):
                        personal_details_serializer.save()
            # Handling Professional Summary
            if request.data.get("professional_summary") is not None:
                professional_summary = request.data.get("professional_summary")
                professional_summary_id = professional_summary.get("id")
                if professional_summary_id is None:
                    professional_summary_serializer = ProfessionalSummarySerializer(data=professional_summary)
                    if professional_summary_serializer.is_valid(raise_exception=True):
                        professional_summary_serializer.save(resume=resume_instance)
                else:
                    try:
                        professional_summary_instance = ProfessionalSummary.objects.get(id=professional_summary_id)
                    except ProfessionalSummary.DoesNotExist:
                        raise Http404
                    professional_summary_serializer = ProfessionalSummarySerializer(professional_summary_instance, data=professional_summary)
                    if professional_summary_serializer.is_valid(raise_exception=True):
                        professional_summary_serializer.save()
            # Handling Complex_section
            # whether exists "complex_sections" key
            if request.data.get("complex_sections") is not None:
                complex_sections = request.data.get("complex_sections")
                for complex_section in complex_sections.values():
                    complex_section_id = complex_section.get("id")
                    # Create a complex section
                    if complex_section_id is None:
                        complex_section_serializer = ComplexSectionSerializer(data=complex_section)
                        if complex_section_serializer.is_valid(raise_exception=True):
                            complex_section_instance = complex_section_serializer.save(resume=resume_instance)
                            # Handling items in the complex_section
                            section_type = complex_section.get("section_type")
                            items = complex_section.get(section_type)
                            for item in items.values():
                                item_id = item.get("id")
                                # Update an item
                                if item_id is not None:
                                    return Response({"details": "Cannot update a item while creating its section"}, status=status.HTTP_400_BAD_REQUEST)
                                # Create an item
                                else:
                                    if section_type == "employment_histories":
                                        item_serializer = EmploymentHistorySerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    elif section_type == "educations":
                                        item_serializer = EducationSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    elif section_type == "skills":
                                        item_serializer = SkillSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    elif section_type == "links":
                                        item_serializer = LinkSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        item_serializer = CustomSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                    # Updating a complex section
                    else:
                        try:
                            complex_section_instance = ComplexSection.objects.get(id=complex_section_id)
                        except ComplexSection.DoesNotExist:
                            raise Http404
                        complex_section_serializer = ComplexSectionSerializer(complex_section_instance, data=complex_section)
                        if complex_section_serializer.is_valid(raise_exception=True):
                            complex_section_instance = complex_section_serializer.save()
                            section_type = complex_section.get("section_type")
                            items = complex_section.get(section_type)
                            if section_type == "employment_histories":
                                for item in items.values():
                                    item_id = item.get("id", None)
                                    if item_id is None:
                                        item_serializer = EmploymentHistorySerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        try:
                                            item_instance = EmploymentHistory.objects.get(id=item_id)
                                        except EmploymentHistory.DoesNotExist:
                                            raise Http404
                                        item_serializer = EmploymentHistorySerializer(item_instance, data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save()
                            elif section_type == "educations":
                                for item in items.values():
                                    item_id = item.get("id", None)
                                    if item_id is None:
                                        item_serializer = EducationSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        try:
                                            item_instance = Education.objects.get(id=item_id)
                                        except Education.DoesNotExist:
                                            raise Http404
                                        item_serializer = EducationSerializer(item_instance, data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save()
                            elif section_type == "skills":
                                for item in items.values():
                                    item_id = item.get("id", None)
                                    if item_id is None:
                                        item_serializer = SkillSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        try:
                                            item_instance = Skill.objects.get(id=item_id)
                                        except Skill.DoesNotExist:
                                            raise Http404
                                        item_serializer = SkillSerializer(item_instance, data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save()
                            elif section_type == "links":
                                for item in items.values():
                                    item_id = item.get("id", None)
                                    if item_id is None:
                                        item_serializer = LinkSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        try:
                                            item_instance = Link.objects.get(id=item_id)
                                        except Link.DoesNotExist:
                                            raise Http404
                                        item_serializer = LinkSerializer(item_instance, data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save()
                            else:  # section_type == "customs"
                                for item in items.values():
                                    item_id = item.get("id", None)
                                    if item_id is None:
                                        item_serializer = CustomSerializer(data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save(complex_section=complex_section_instance)
                                    else:
                                        try:
                                            item_instance = Custom.objects.get(id=item_id)
                                        except Custom.DoesNotExist:
                                            raise Http404
                                        item_serializer = CustomSerializer(item_instance, data=item)
                                        if item_serializer.is_valid(raise_exception=True):
                                            item_serializer.save()
            return Response(resume_serializer.data, status=status.HTTP_201_CREATED)
        return Response(resume_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = "pk"  # Default


class ResumeDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, format=None):
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeListSerializer(resumes, many=True)
        return Response(serializer.data)


class ResumeDuplicate(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, pk, format=None):
        try:
            original_resume = Resume.objects.get(id=pk)
        except Resume.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, original_resume)

        original_personal_details = original_resume.personal_details if hasattr(original_resume, "personal_details") else None
        original_professional_summary = original_resume.professional_summary if hasattr(original_resume, "professional_summary") else None
        original_complex_sections = original_resume.complex_sections.all() if hasattr(original_resume, "complex_sections") else []

        # make a copy of the original resume
        copy_resume = copy.deepcopy(original_resume)
        copy_resume.pk = None
        copy_resume._state.adding = True
        copy_resume.title = "Copy of " + copy_resume.title
        copy_resume.save()
        # make a copy of personal details
        if original_personal_details:
            original_personal_details.pk = None
            original_personal_details._state.adding = True
            original_personal_details.resume = copy_resume
            original_personal_details.save()
        # make a copy of professional summary
        if original_professional_summary:
            original_professional_summary.pk = None
            original_professional_summary._state.adding = True
            original_professional_summary.resume = copy_resume
            original_professional_summary.save()
        # make a copy of all complex sections
        for original_complex_section in original_complex_sections:
            copy_complex_section = copy.deepcopy(original_complex_section)
            copy_complex_section.pk = None
            copy_complex_section._state.adding = True
            copy_complex_section.resume = copy_resume
            copy_complex_section.save()

            # section_type_object = ComplexSection._meta.get_field("section_type")
            # section_type_value = section_type_object.value_from_object(original_complex_section)
            section_type_value = original_complex_section.section_type
            if section_type_value == "employment_histories":
                original_complex_section_items = original_complex_section.employment_histories.all()
            elif section_type_value == "educations":
                original_complex_section_items = original_complex_section.educations.all()
            elif section_type_value == "skills":
                original_complex_section_items = original_complex_section.skills.all()
            elif section_type_value == "links":
                original_complex_section_items = original_complex_section.links.all()
            else:  # customs section
                original_complex_section_items = original_complex_section.customs.all()
            for orginal_complex_section_item in original_complex_section_items:
                orginal_complex_section_item.pk = None
                orginal_complex_section_item._state.adding = True
                orginal_complex_section_item.complex_section = copy_complex_section
                orginal_complex_section_item.save()
        resume_serializer = ResumeSerializer(copy_resume)
        return Response(resume_serializer.data, status=status.HTTP_200_OK)


class ResumeImagesUploading(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Resume.objects.all()
    serializer_class = ImagesUploadingSerializer
