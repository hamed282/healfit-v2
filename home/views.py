from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (BannerSliderModel, CommentHomeModel, VideoHomeModel, ContentHomeModel, BannerShopModel, LogoModel,
                     SEOHomeModel, NewsLetterModel)
from .serializers import (BannerSliderSerializer, CommentHomeSerializer, VideoHomeSerializer, ContentHomeSerializer,
                          BannerShopSerializer, SEOHomeSerializer, LogoHomeSerializer, NewsLetterSerializer)


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


class LogoHomeView(APIView):
    def get(self, request):
        logo = LogoModel.objects.all()
        ser_data = LogoHomeSerializer(instance=logo, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SEOHomeView(APIView):
    def get(self, request):
        seo = SEOHomeModel.objects.all()
        ser_data = SEOHomeSerializer(instance=seo, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class NewsLetterView(APIView):

    def post(self, request):
        form = request.data

        ser_data = NewsLetterSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
