from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings 

from .parser.rule_based_parser import RuleBasedParser
from .parser.chat_gpt_parser import ChatGPTParser
from .parser.bart_parser import BartParser

import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tesseract_version = pytesseract.get_tesseract_version()
print("tesseract_version", tesseract_version.base_version)

cache_folder = "cache_parse_resume/"

# chatgpt_parser = ChatGPTParser()
chatgpt_parser = None
bart_parser = BartParser() if settings.ENABLE_BART else None

rulebased_parser = RuleBasedParser()

class ParseResume(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data['userId']
            file = request.data['file']
            file_type = request.data['fileType']
            parse_type = request.data['parseType']
            # handler
            filename = cache_folder + userid + ".png"
            tmp_file = self.save_cache_file(filename, file)
            if chatgpt_parser != None and parse_type == "chatgpt":
                parser = chatgpt_parser
            elif bart_parser != None and parse_type == "bart":
                parser = bart_parser
            else:
                parser = rulebased_parser
            if file_type == "pdf":
                raw_text = self.pdf_to_text(tmp_file)
            else:
                raw_text = self.image_to_text(tmp_file)           
            result = parser.parse(raw_text)
            # self.clear_cache_file(tmp_file)
            return Response(data=result, status=status.HTTP_200_OK)
        
        except Exception as e:
            raise e
            return Response(data={'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def save_cache_file(self, filename, file):
        path = default_storage.save(filename, ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        return tmp_file

    def clear_cache_file(self, tmp_file):
        os.remove(tmp_file)
        split = tmp_file.split('.')
        os.remove(''.join(split[:-1]) + '_scaled' + "." + split[-1])


    def image_to_text(self, image_path):
        image_root = cv2.imread(image_path)
        image_size = (1414, 2000)
        image = cv2.resize(image_root, image_size, interpolation= cv2.INTER_LINEAR)
        split = image_path.split('.')
        cv2.imwrite(''.join(split[:-1]) + "_scaled" + "." + split[-1], image)
        np_array = np.array(image, dtype=np.uint8)
        text = pytesseract.image_to_string(np_array)
        return text
    
    def pdf_to_text(self, pdf_file):
        image = convert_from_path(pdf_file)[0]
        split = pdf_file.split('.')
        image_path = ''.join(split[:-1]) + '.png'
        image.save(image_path)
        return self.image_to_text(image_path)