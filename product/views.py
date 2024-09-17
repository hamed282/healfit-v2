from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (ProductGenderModel, ProductModel, SizeProductModel, ColorProductModel, ProductVariantModel,
                     AddImageGalleryModel, PopularProductModel, ProductCategoryModel, ProductSubCategoryModel,
                     FavUserModel, CouponModel)
from .serializers import (ProductGenderSerializer, ProductSerializer, ProductVariantShopSerializer,
                          ProductColorImageSerializer, ColorSizeProductSerializer, ProductListSerializer,
                          UserFavSerializer, PopularProductSerializer, ProductAllSerializer,
                          ProductCategorySerializer, ProductSubCategorySerializer, ProductByCategorySerializer,
                          FavProductSerializer)
from django.shortcuts import get_object_or_404
from math import ceil
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .service import Cart
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal
import uuid


class ProductGenderView(APIView):

    def get(self, request):
        gender_category = ProductGenderModel.objects.filter(gender__in=['men', 'women'])
        ser_gender_category = ProductGenderSerializer(instance=gender_category, many=True)

        return Response(data=ser_gender_category.data)


class ProductView(APIView):
    def get(self, request):
        product_slug = self.request.query_params.get('slug', None)
        if product_slug is not None:
            product = get_object_or_404(ProductModel, slug=product_slug)
            ser_product = ProductSerializer(instance=product)
            return Response(data=ser_product.data)
        else:
            return Response(data={'massage': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantShopView(APIView):
    """
    note: get product variant price
    queries:
    1. product
    2. size
    3. color
    """
    def get(self, request):
        product_name = self.request.query_params.get('product', None)
        product_size = self.request.query_params.get('size', None)
        product_color = self.request.query_params.get('color', None)
        if product_name is not None and product_size is not None and product_color is not None:
            product_name = ProductModel.objects.get(product=product_name)
            product_size = SizeProductModel.objects.get(size=product_size)
            product_color = ColorProductModel.objects.get(color=product_color)
            product = get_object_or_404(ProductVariantModel, product=product_name, size=product_size, color=product_color)
            ser_product = ProductVariantShopSerializer(instance=product)
            return Response(data=ser_product.data)
        else:
            return Response(data={'massage': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class ProductColorImageView(APIView):
    """
    queryset:
    1. product
    2. color
    """
    def get(self, request):
        product = self.request.query_params.get('product', None)
        product = ProductModel.objects.get(product=product)

        color = self.request.query_params.get('color', None)
        product_color = ColorProductModel.objects.get(color=color)

        images = AddImageGalleryModel.objects.filter(product=product, color=product_color)
        ser_data = ProductColorImageSerializer(many=True, instance=images)
        return Response(data=ser_data.data)


class ColorSizeProductView(APIView):
    def get(self, request):
        product_size = self.request.query_params.get('size', None)
        product_slug = self.request.query_params.get('slug', None)

        product = ProductModel.objects.get(slug=product_slug)
        size = SizeProductModel.objects.get(size=product_size)
        color = product.product_color_size.filter(size=size, quantity__gt=0)
        ser_data = ColorSizeProductSerializer(instance=color, many=True)

        return Response(data=ser_data.data)


class SizeOfColorView(APIView):
    def get(self, request):
        product_query = self.request.query_params.get('product', None)

        product = ProductModel.objects.get(product=product_query)

        color_query = self.request.query_params.get('color', None)
        color = ColorProductModel.objects.get(color=color_query)

        products = ProductVariantModel.objects.filter(product=product, color=color, quantity__gt=0)
        sizes = []
        for product in products:
            sizes.append(product.size.size)
        return Response(data=sizes)


class ProductGenderListView(APIView):
    def get(self, request):
        """
        get parameter:
        1. page_number
        2. slug
        3. limit
        """

        page_number = int(self.request.query_params.get('page_number', 1))
        gender_slug = self.request.query_params.get('slug', None)
        per_page = self.request.query_params.get('limit', 16)

        gender = get_object_or_404(ProductGenderModel, slug=gender_slug)
        unisex = get_object_or_404(ProductGenderModel, slug='unisex')

        products_count = len(ProductModel.objects.filter(gender__in=[gender, unisex]))

        number_of_pages = ceil(products_count/per_page)
        if page_number is not None:
            product_list = ProductModel.objects.filter(gender__in=[gender, unisex]).order_by('priority')[per_page*(page_number-1):per_page*page_number]
        else:
            product_list = ProductModel.objects.filter(gender__in=[gender, unisex]).order_by('priority')

        ser_product_list = ProductListSerializer(instance=product_list, many=True)
        category_title = gender.gender

        return Response(data={'data': ser_product_list.data, 'title': category_title, 'number_of_pages': number_of_pages})


class ProductAllView(APIView):
    def get(self, request):
        """
        get parameter:
        1. page_number
        3. limit
        """
        page_number = int(self.request.query_params.get('page_number', 1))
        per_page = int(self.request.query_params.get('limit', 16))
        gender = self.request.query_params.get('gender', None)
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)
        available = self.request.query_params.get('available', None)

        size = self.request.query_params.get('size', None)
        if size:
            size = size.split(',')

        color = self.request.query_params.get('color', None)
        if color:
            color = color.split(',')

        try:
            available = available.lower() in ['true', '1']
        except:
            available = False
        products = ProductModel.filter_products(
            gender=gender,
            color=color,
            size=size,
            category=category,
            subcategory=subcategory,
            available=available
        )

        products_count = len(products)
        number_of_pages = ceil(products_count / per_page)

        if page_number is not None:
            product_list = products.order_by('priority')[per_page * (page_number - 1):per_page * page_number]
        else:
            product_list = products.order_by('priority')

        ser_product_list = ProductAllSerializer(instance=product_list, many=True, context={'request': request})

        return Response(data={'data': ser_product_list.data, 'number_of_pages': number_of_pages})


class SearchProductView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductAllSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product', 'name_product', 'application_fields']
    ordering_fields = '__all__'


class PopularProductView(APIView):
    def get(self, request):
        popular_product = PopularProductModel.objects.all()
        ser_popular_product = PopularProductSerializer(instance=popular_product, many=True)

        return Response(data=ser_popular_product.data)


class CategoryItemView(APIView):
    def get(self, request, slug_category):
        page_number = int(self.request.query_params.get('page_number', 1))
        per_page = int(self.request.query_params.get('limit', 16))

        category = ProductCategoryModel.objects.get(slug=slug_category)
        products = category.category_product.all()

        products_count = len(products)
        number_of_pages = ceil(products_count/per_page)

        if page_number is not None:
            product_list = products[per_page * (page_number - 1):per_page * page_number]
        else:
            product_list = products

        ser_data = ProductByCategorySerializer(instance=product_list, many=True)
        return Response(data={'data': ser_data.data, 'number_of_pages': number_of_pages}, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    def get(self, request):
        categories = ProductCategoryModel.objects.all()
        ser_data = ProductCategorySerializer(instance=categories, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CategoryFilterView(APIView):
    def get(self, request, slug_category):
        category = ProductCategoryModel.objects.get(slug=slug_category)
        ser_data = ProductCategorySerializer(instance=category)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CategoryBySubcategoryView(APIView):
    def get(self, request, slug_category):
        category = ProductCategoryModel.objects.get(slug=slug_category)
        subcategories = ProductSubCategoryModel.objects.filter(category=category)
        ser_data = ProductSubCategorySerializer(instance=subcategories, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SubcategoryListView(APIView):
    def get(self, request):
        subcategories = ProductSubCategoryModel.objects.all()
        ser_data = ProductSubCategorySerializer(instance=subcategories, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SubcategoryItemView(APIView):
    def get(self, request, slug_subcategory):
        page_number = int(self.request.query_params.get('page_number', 1))
        per_page = int(self.request.query_params.get('limit', 16))

        subcategory = ProductSubCategoryModel.objects.get(slug=slug_subcategory)
        products = subcategory.subcategory_product.all()

        products_count = len(products)
        number_of_pages = ceil(products_count/per_page)

        if page_number is not None:
            product_list = products[per_page * (page_number - 1):per_page * page_number]
        else:
            product_list = products

        ser_data = ProductByCategorySerializer(instance=product_list, many=True)
        return Response(data={'data': ser_data.data, 'number_of_pages': number_of_pages}, status=status.HTTP_200_OK)


class SubcategoryFilterView(APIView):
    def get(self, request, slug_subcategory):
        subcategory = ProductSubCategoryModel.objects.get(slug=slug_subcategory)
        ser_data = ProductSubCategorySerializer(instance=subcategory)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ProductItemView(APIView):
    def get(self, request, slug_product):
        product = ProductModel.objects.get(slug=slug_product)
        ser_data = ProductSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class FavProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        fav = FavUserModel.objects.get(product=ProductModel.objects.get(id=product_id), user=request.user)
        ser_data = FavProductSerializer(instance=fav)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavProductSerializer(data=request.data, context={'request': request, 'product_id': request.data['product']})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        if product_id is None:
            return Response(data={'message': 'Input product ID'})
        try:
            product = FavUserModel.objects.get(product=ProductModel.objects.get(id=product_id), user=request.user)
        except:
            return Response(data={'message': 'product is not exist'})

        product.delete()

        return Response(data={'message': f'The fav product ID {product} was deleted'}, status=status.HTTP_200_OK)


class UserFavView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_fav = FavUserModel.objects.filter(user=request.user)
        ser_data = UserFavSerializer(instance=product_fav, many=True, context={'request': request})
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CartView(APIView):
    def get(self, request, format=None):
        # بررسی اینکه آیا شناسه سبد خرید در کوکی‌ها موجود است
        # cart_id = request.COOKIES.get('cart_id')
        #
        # if not cart_id:
        #     return Response({"message": "Cart is empty."}, status=status.HTTP_200_OK)

        cart = Cart(request)

        return Response(
            {
                "data": list(cart.__iter__()),
                "cart_total_price": cart.get_total_price()
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        """
        parameters:
        1. product # course id
            - id
            - off_price
        2. quantity # product order
        3. remove # true
        4. clear # true
        ۵. discount_code # a code
        """

        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

            response = JsonResponse({"message": 'cart removed', "cart_total_items": cart.get_total_items()})
            response.delete_cookie('cart_id')
            return response

        elif "clear" in request.data:
            cart.clear()

            response = JsonResponse({"message": 'cart cleaned', "cart_total_items": cart.get_total_items()})
            response.delete_cookie('cart_id')
            return response

        elif "discount_code" in request.data:
            discount_code = request.data["discount_code"]

            try:
                # پیدا کردن کد تخفیف در دیتابیس
                code = CouponModel.objects.get(coupon_code=discount_code)

                # بررسی معتبر بودن کد
                if code.is_valid():
                    discount_percent = Decimal(code.discount_percent)
                    data = list(cart.__iter__()),
                    total_price = cart.get_total_price()

                    # محاسبه قیمت پس از اعمال تخفیف
                    discounted_price = total_price - (total_price * discount_percent / Decimal('100'))

                    # بازگرداندن نتیجه به کاربر
                    return JsonResponse({
                        "message": "Code applied successfully! your total has been updated.",
                        "data": data,
                        "total_price": str(total_price),
                        "discounted_price": str(discounted_price),
                        "cart_total_items": cart.get_total_items(),
                    })

                else:
                    return JsonResponse({"message": "The promo code isn't valid. Please verify the code and try again."},
                                        status=status.HTTP_400_BAD_REQUEST)

            except CouponModel.DoesNotExist:
                return JsonResponse({"message": "The promo code isn't valid. Please verify the code and try again."},
                                    status=status.HTTP_400_BAD_REQUEST)

        else:
            product = request.data
            add = cart.add(
                product=product["product"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

            response = JsonResponse({"message": add['massage'], "cart_total_items": cart.get_total_items()})
            expires = datetime.now() + timedelta(days=365)  # انقضا پس از 1 سال
            unique_cart_id = str(uuid.uuid4())  # ایجاد یک شناسه تصادفی منحصربه‌فرد

            # response.set_cookie('cart_id', unique_cart_id, expires=expires)
            # response.set_cookie(
            #     'cart_id',  # نام کوکی
            #     unique_cart_id,  # مقدار کوکی
            #     expires=expires,  # تاریخ انقضای کوکی
            #     httponly=False,  # اگر نیاز دارید که جاوااسکریپت به کوکی دسترسی داشته باشد، این را False بگذارید
            #     secure=True,  # برای HTTPS باید True باشد
            #     samesite='None'  # یا 'None' اگر cross-origin است
            # )
            response.set_cookie(
                'cart_id',
                unique_cart_id,
                expires=expires,
                path='/',  # در کل دامنه در دسترس باشد
                domain='.healfit.ae',  # دسترسی به کوکی برای هر دو دامنه اصلی و ساب‌دامنه‌ها
                secure=True,  # برای HTTPS ضروری
                httponly=False,  # اگر به جاوااسکریپت نیاز دارید که به کوکی دسترسی داشته باشد
                samesite='None'  # برای Cross-Origin Requests
            )

            return response


# class CartView(APIView):
#     def get(self, request, format=None):
#         cart = Cart(request)
#
#         return Response(
#             {"data": list(cart.__iter__()),
#              "cart_total_price": cart.get_total_price()
#              },
#             status=status.HTTP_200_OK
#             )
#
#     def post(self, request, **kwargs):
#         """
#         parameters:
#         1. product # course id
#             - id
#             - off_price
#         2. quantity # product order
#         3. remove # true
#         4. clear # true
#         """
#
#         cart = Cart(request)
#         if "remove" in request.data:
#             product = request.data["product"]
#             cart.remove(product)
#
#             return Response(
#                 {"message": 'cart removed'},
#                 status=status.HTTP_202_ACCEPTED)
#
#         elif "clear" in request.data:
#             cart.clear()
#
#             return Response(
#                 {"message": 'cart cleaned'},
#                 status=status.HTTP_202_ACCEPTED)
#
#         else:
#             product = request.data
#             add = cart.add(
#                 product=product["product"],
#                 quantity=product["quantity"],
#                 overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
#             )
#
#             return Response(
#                 {"message": add['massage']},
#                 status=status.HTTP_202_ACCEPTED)
