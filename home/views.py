from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BannerSliderModel, CommentHomeModel, VideoHomeModel
from .serializers import BannerSliderSerializer, CommentHomeSerializer, VideoHomeSerializer


class ImageSliderView(APIView):
    def get(self, request):
        banner_slider = BannerSliderModel.objects.all()
        ser_data = BannerSliderSerializer(instance=banner_slider, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class VideoHomeView(APIView):
    def get(self, request):
        video = VideoHomeModel.objects.all()
        ser_data = VideoHomeSerializer(instance=video, many=True)
        return Response(data=ser_data.data)


class CommentHomeView(APIView):
    def get(self, request):
        comment = CommentHomeModel.objects.all()
        ser_data = CommentHomeSerializer(instance=comment, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
