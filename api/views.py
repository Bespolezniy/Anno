from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView

from main.models import Anno, Comment
from .serializers import AnnoSerializer, AnnoDetailSerializer, CommentSerializer

# Create your views here.
@api_view(['GET'])
def anno(request):

    if request.method == 'GET':
        anno = Anno.objects.filter(is_active=True)[:10]
        serializer = AnnoSerializer(anno, many=True)
        return Response(serializer.data) 


class AnnoDetailView(RetrieveAPIView):
    queryset = Anno.objects.filter(is_active=True)
    serializer_class = AnnoDetailSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, anno=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data) 

