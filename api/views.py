from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import apiSerializer, apiViewSerializer
from .models import api
import requests

class apiViewSet(APIView):
    def post(self, request):
        serializer = apiSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status_code":status.HTTP_201_CREATED,"status": "success","data":request.data})
        else:
            return Response({"status_code":status.HTTP_400_BAD_REQUEST,"status": "error","data":request.data})
    
    def get(self, request, id = None):
        if id:
            try:
                item = api.objects.get(id=id)
                serializer = apiSerializer(item)
                return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": serializer.data})
            except Exception as e:
                return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": []})

        try:
            items = api.objects.all()
            serializer = apiSerializer(items, many=True)
            return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": serializer.data})
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": []})
    
    def delete(self, request, id=None):
        try:
            item = get_object_or_404(api, id=id)
            name = item.name
            item.delete()
            return Response({"status_code": status.HTTP_200_OK, "status":"success","message":"The book {} was deleted successfully".format(name), "data":[]})
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK, "status":"Id does not exist", "data": []})

    def patch(self, request, id=None):
        item = api.objects.get(id=id)
        serializer = apiSerializer(item, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status_code":status.HTTP_201_CREATED,"status": "success","data":request.data})
        else:
            return Response({"status_code":status.HTTP_400_BAD_REQUEST,"status": "error","data":request.data})

class apiExternalView(APIView):
    def get(self, request, id = None):
        try:
            if id==None:
                name = request.GET.get('name',None)
                items = requests.get("https://anapioficeandfire.com/api/books?name="+name).json()
                data = []
                for item in items:
                    data.append({'name':item['name'],'isbn':item['isbn'],'authors':item['authors'],'number_of_pages':item['numberOfPages'],'publisher':item['publisher'],'country':item['country'],'release_date':item['released']})
                serializer = apiViewSerializer(data, many=True).data
                return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": serializer})
            else:
                item = requests.get("https://anapioficeandfire.com/api/books/"+str(id)).json()
                data = []
                data.append({'name':item['name'],'isbn':item['isbn'],'authors':item['authors'],'number_of_pages':item['numberOfPages'],'publisher':item['publisher'],'country':item['country'],'release_date':item['released']})
                serializer = apiViewSerializer(data, many=True).data
                return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": serializer})
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK, "status":"success", "data": []})