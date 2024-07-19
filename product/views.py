from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductGenderModel
from .serializers import ProductGenderSerializer


class ProductGenderView(APIView):

    def get(self, request):
        gender_category = ProductGenderModel.objects.filter(gender__in=['men', 'women'])
        ser_gender_category = ProductGenderSerializer(instance=gender_category, many=True)

        return Response(data=ser_gender_category.data)





