from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializer import EssaySerializer , AlbumSerializer, FileSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]    
    search_fields = ('title','body',)


    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.filter(author=self.request.user)
        else:
            qs = qs.none()
        return qs

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

from rest_framework.response import Response

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if seializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)