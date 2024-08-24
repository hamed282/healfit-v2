from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BannerSliderModel, CommentHomeModel, VideoHomeModel, ContentHomeModel, BannerShopModel
from .serializers import (BannerSliderSerializer, CommentHomeSerializer, VideoHomeSerializer, ContentHomeSerializer,
                          BannerShopSerializer)


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
        comment = CommentHomeModel.objects.filter(active=True)
        ser_data = CommentHomeSerializer(instance=comment, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class HomeContentView(APIView):
    def get(self, request):
        content = ContentHomeModel.objects.all().first()
        ser_data = ContentHomeSerializer(instance=content)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BannerShopView(APIView):
    def get(self, request):
        banners = BannerShopModel.objects.all()
        ser_data = BannerShopSerializer(instance=banners, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
