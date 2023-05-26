import abc
from datetime import date, timedelta

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
    pagination_class = LimitOffsetPagination
    queryset = JobPosting.objects.all()


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

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
            sort = request.data.get("sort")
            if sort == "newest":
                search = self.document_class.search().query(q).sort({"date": {"order": "desc"}})
            else:
                search = self.document_class.search().query(q)
            print("hello")
            total = search.count()
            search = search[0:total]
            response = search.execute()

            # print(f"Found {response.hits.total.value} hit(s) for query: "{query}"")

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
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
        print(title)
        print(loc)
        must_list = [
            Q("match_phrase", searching_location=loc),
            Q("match", job_title=title)
        ]
        should_list = [
            Q("match", details=title)
        ]
        filter_list = []
        keywords = query.get("keywords")
        print(keywords)
        if keywords:
            must_list.append(Q(
                "bool",
                should=[Q("match_phrase", details=keyword) for keyword in keywords]
            ))
        job_portal = query.get("job_portal")
        print(job_portal)
        if job_portal:
            job_portal = " ".join(job_portal)
            filter_list.append(Q("match", job_portal=job_portal))
        last_updated = query.get("last_updated")
        print(last_updated)
        if last_updated and int(last_updated) != 0:
            date_mark = date.today() - timedelta(days=int(last_updated))
            filter_list.append(Q(
                "range",
                date={
                    "gte": date_mark
                }
            ))
        return Q(
            "bool",
            must=must_list,
            should=should_list,
            filter=filter_list,
        )
