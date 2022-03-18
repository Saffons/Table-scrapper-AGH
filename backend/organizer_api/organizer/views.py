from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ScrapSerializer
from .models import Scrap
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import cv2
from image_to_csv import image_to_csv


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/scrap-list/',
        'Create':'/scrap-create/',
        'Delete':'/scrap-delete/<str:pk>/'
    }
    
    return Response(api_urls)

@csrf_exempt
def Api(request, iid=0):
    if request.method=='GET':
        scraps = Scrap.objects.all()
        scraps_serializer = ScrapSerializer(scraps, many=True)
        return JsonResponse(scraps_serializer.data, safe=False)
    elif request.method=='POST':
        scrap_data = JSONParser().parse(request)
        scrap_serializer = ScrapSerializer(data = scrap_data)
        if scrap_serializer.is_valid():
            scrap_serializer.save()
            return JsonResponse("added", safe=False)
        return JsonResponse("failed post", safe = False)
    elif request.method=='PUT':
        scrap_data = JSONParser().parse(request)
        scrap = Scrap.objects.get(id=scrap_data['id'])
        scrap_serializer = ScrapSerializer(scrap, data=scrap_data)
        if scrap_serializer.is_valid():
            scrap_serializer.save()
            return JsonResponse("updated", safe = False)
        return JsonResponse("Failed put", safe = False)
    elif request.method=='DELETE':
        scrap = Scrap.objects.get(id=iid)
        scrap.delete()
        return JsonResponse("Deleted succesfully", safe=False)
    
@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    image = cv2.imread("../../db/" + file.name)
    csvv = image_to_csv(image)
    with open("../../db/"+file.name+".csv", 'w') as f:
        f.write(csvv)

    return JsonResponse(csvv, safe=False)
