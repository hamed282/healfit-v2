from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BannerSliderModel
from .serializers import BannerSliderSerializer


class ImageSliderView(APIView):
    def get(self, request):
        banner_slider = BannerSliderModel.objects.all()
        ser_data = BannerSliderSerializer(instance=banner_slider, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)



