import os
import sys
import json

import grpc
from ai_bridge.protos import resume_builder_ai_service_pb2
from ai_bridge.protos import resume_builder_ai_service_pb2_grpc
from django.conf import settings

# HOST = "tlt-resume-builder-ai-helper.icyisland-dd584dc3.southeastasia.azurecontainerapps.io" # 
# HOST = "127.0.0.1:50052"
HOST = settings.AI_SERVICE_HOST

class Client:
    def __init__(self):
        # self.channel = grpc.insecure_channel(HOST)
        creds = grpc.ssl_channel_credentials()
        self.channel = grpc.secure_channel(HOST, creds)
        self.stub = resume_builder_ai_service_pb2_grpc.ResumeAIServiceStub(self.channel)
        print("Init connect to server AI finish")

    def parse_resume(self, filename, filetype, parsetype, base64data):
        request = resume_builder_ai_service_pb2.ParseResumeRequest(
            filename=filename,
            filetype=filetype,
            parsetype=parsetype,
            base64data=base64data
        )
        response = self.stub.ParseResume(request) 
        result = json.loads(response.result)
        return result

    def suggestion_summary(self, input):
        request = resume_builder_ai_service_pb2.SuggestionSummaryRequest(
            input=input
        )
        response = self.stub.SuggestionSummary(request)
        suggestions = response.output.split('|')
        print(suggestions)
        return suggestions
    
ai_agent = Client()