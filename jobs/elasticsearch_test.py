from elasticsearch_dsl import Q
from jobs.documents import JobPostingDocument


job_title = 'python developer'
loc = 'Ho Chi Minh city, Vietnam'
q = Q(
    'bool',
    must=[
        Q('match_phrase', searching_location=loc),
        Q('match', job_title=job_title)
    ],
    should=[
        Q('match', details=job_title)
    ]
)
search = JobPostingDocument.search().query(q)
print(search)
response = search.execute()
print(response)
print("hits: ", response.hits.total.value)

# print all the hits
for hit in search:
    print(hit.id)
