import abc

from django.http import HttpResponse

from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from elasticsearch_dsl import Q

from .serializers import JobPostingSerializer
from .documents import JobPostingDocument
from .models import JobPosting


class JobPostingListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = JobPostingSerializer
    queryset = JobPosting.objects.all()


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None
    # pagination_class = LimitOffsetPagination

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def post(self, request):
        try:
            query = request.data.get("query")
            q = self.generate_q_expression(query)
            # search = self.document_class.search().extra(size=100).query(q)
            # More consideration: How to control the number of hits returned from Elastic
            search = self.document_class.search().query(q)
            total = search.count()
            search = search[0:total]
            response = search.execute()
            print("hello", response[0].date)

            # print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            print(results[0].date)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
            # return Response(response.to_dict(), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)


class JobSearchingAPIView(PaginatedElasticSearchAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = JobPostingSerializer
    document_class = JobPostingDocument

    def generate_q_expression(self, query):
        title = query.get("job_title")
        loc = query.get("location")
        return Q(
            'bool',
            must=[
                Q('match_phrase', searching_location=loc),
                Q('match', job_title=title)
            ],
            should=[
                Q('match', details=title)
            ]
        )
