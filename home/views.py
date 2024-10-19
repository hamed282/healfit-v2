from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (BannerSliderModel, CommentHomeModel, VideoHomeModel, ContentHomeModel, BannerShopModel, LogoModel,
                     SEOHomeModel, ContactSubmitModel)
from .serializers import (BannerSliderSerializer, CommentHomeSerializer, VideoHomeSerializer, ContentHomeSerializer,
                          BannerShopSerializer, SEOHomeSerializer, LogoHomeSerializer, NewsLetterSerializer,
                          ContactSubmitSerializer)
from django.conf import settings
from django.core.mail import send_mail


class ImageSliderView(APIView):
    def get(self, request):
        from order.models import OrderModel, OrderItemModel
        from utils import send_order_email
        order = OrderModel.objects.get(id=38)
        order_items = OrderItemModel.objects.filter(order=order)

        recipient_list = ['hamed.alizadegan@gmail.com']
        send_order_email(order, order_items, recipient_list)

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


class ContactView(APIView):
    def post(self, request):
        """
        parameters:
        1. first_name
        2. last_name
        3. email
        4. mobile
        5. message
        """
        form = request.data
        ser_submit = ContactSubmitSerializer(data=form)
        if ser_submit.is_valid():
            ContactSubmitModel.objects.create(first_name=form['first_name'],
                                              last_name=form['last_name'],
                                              email=form['email'],
                                              mobile=form['mobile'],
                                              message=form['message'])

            subject = 'welcome to Healfit'
            message_customer = 'Hi Wellcome to healfit'
            message_provider = f'full name: {form["first_name"]} {form["last_name"]} \n' \
                               f'emai: {form["email"]} \n' \
                               f'mobile: {form["mobile"]} \n' \
                               f'Message: {form["message"]}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form['email']]

            send_mail(subject, message_customer, email_from, recipient_list)
            send_mail(subject, message_provider, email_from, ['no-reply@healfit.ae'])

            return Response(data={'message': 'successfully submitted'})
        else:
            return Response(data=ser_submit.errors)
