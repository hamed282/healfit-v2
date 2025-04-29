from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (BannerSliderModel, CommentHomeModel, VideoHomeModel, Content1Model, Content2Model, Content3Model, BannerShopModel, LogoModel,
                     SEOHomeModel, ContactSubmitModel, TelegramBotModel, AboutPageModel, CareerPageModel, BlogPageModel,
                     ShopPageModel, SitemapPageModel, WholesaleInquiryPageModel, CustomerCarePageModel,
                     RefundPolicyPageModel, ContactUsPageModel, BannerSliderMobileModel)
from .serializers import (BannerSliderSerializer, CommentHomeSerializer, VideoHomeSerializer, ContentHome1Serializer,
                          BannerShopSerializer, SEOHomeSerializer, LogoHomeSerializer, NewsLetterSerializer,
                          ContactSubmitSerializer, AboutPageSerializer, ShopPageSerializer, BlogPageSerializer,
                          CareerPageSerializer, SitemapPageSerializer, ContactUsPageSerializer,
                          RefundPolicyPageSerializer, WholesaleInquiryPageSerializer, CustomerCarePageSerializer,
                          ContentHome2Serializer, ContentHome3Serializer)
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from services.sitemapPage import sitemap


class ImageSliderView(APIView):
    def get(self, request):
        banner_slider = BannerSliderModel.objects.filter(active=True).order_by('priority')
        banner_slider_mobile = BannerSliderMobileModel.objects.filter(active=True).order_by('priority')

        ser_data = BannerSliderSerializer(instance=banner_slider, many=True)
        ser_data_mobile = BannerSliderSerializer(instance=banner_slider_mobile, many=True)

        return Response(data={'desktop': ser_data.data, 'mobile': ser_data_mobile.data}, status=status.HTTP_200_OK)


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
        content1 = Content1Model.objects.all().first()
        content2 = Content2Model.objects.all().first()
        content3 = Content3Model.objects.all().first()
        
        ser_data1 = ContentHome1Serializer(instance=content1)
        ser_data2 = ContentHome2Serializer(instance=content2)
        ser_data3 = ContentHome3Serializer(instance=content3)
        
        return Response(data={
            'content1': ser_data1.data,
            'content2': ser_data2.data,
            'content3': ser_data3.data
        }, status=status.HTTP_200_OK)


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
            send_mail(subject, message_provider, email_from, ['hamed@healfit.ae', 'info@healfit.ae'])

            return Response(data={'message': 'successfully submitted'})
        else:
            return Response(data=ser_submit.errors)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message and message.get('text') == '/start':
                chat_id = message['chat']['id']
                username = message['from'].get('username')

                user, created = TelegramBotModel.objects.get_or_create(chat_id=chat_id)
                if username:
                    user.username = username
                user.save()

                return JsonResponse({'status': 'success', 'created': created})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'failed'})


class SiteMapView(APIView):
    def get(self, request):
        data = sitemap()
        return Response(data=data, status=status.HTTP_200_OK)


class AboutPageView(APIView):
    def get(self, request):
        about = AboutPageModel.objects.all().first()
        ser_data = AboutPageSerializer(instance=about)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ContactUsPageView(APIView):
    def get(self, request):
        contact = ContactUsPageModel.objects.all().first()
        ser_data = ContactUsPageSerializer(instance=contact)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CustomerCarePageView(APIView):
    def get(self, request):
        customer = CustomerCarePageModel.objects.all().first()
        ser_data = CustomerCarePageSerializer(instance=customer)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class WholesaleInquiryPageView(APIView):
    def get(self, request):
        wholesale = WholesaleInquiryPageModel.objects.all().first()
        ser_data = WholesaleInquiryPageSerializer(instance=wholesale)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class RefundPolicyPageView(APIView):
    def get(self, request):
        refund = RefundPolicyPageModel.objects.all().first()
        ser_data = RefundPolicyPageSerializer(instance=refund)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SitemapPageView(APIView):
    def get(self, request):
        sitemap_page = SitemapPageModel.objects.all().first()
        ser_data = SitemapPageSerializer(instance=sitemap_page)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CareerPageView(APIView):
    def get(self, request):
        career = CareerPageModel.objects.all().first()
        ser_data = CareerPageSerializer(instance=career)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ShopPageView(APIView):
    def get(self, request):
        shop = ShopPageModel.objects.all().first()
        ser_data = ShopPageSerializer(instance=shop)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BlogPageView(APIView):
    def get(self, request):
        blog = BlogPageModel.objects.all().first()
        ser_data = BlogPageSerializer(instance=blog)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
