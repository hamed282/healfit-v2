from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (ProductGenderModel, ProductModel, SizeProductModel, ColorProductModel, ProductVariantModel,
                     AddImageGalleryModel, PopularProductModel, ProductCategoryModel, ProductSubCategoryModel,
                     FavUserModel, CouponModel, CompressionClassModel, SideModel, CustomerTypeModel, ProductTypeModel,
                     BodyAreaModel, ClassNumberModel, TreatmentCategoryModel, HearAboutUsModel, CustomMadePageModel,
                     BrandCartModel, ProductBrandModel, CustomMadeAttachFileModel)
from .serializers import (ProductGenderSerializer, ProductSerializer, ProductVariantShopSerializer,
                          ProductColorImageSerializer, ColorSizeProductSerializer, ProductListSerializer,
                          UserFavSerializer, PopularProductSerializer, ProductAllSerializer,
                          ProductCategorySerializer, ProductSubCategorySerializer, ProductByCategorySerializer,
                          FavProductSerializer, GetClassSerializer, NewProductSerializer, CategoryBestSellerSerializer,
                          CustomMadeSerializer, CustomMadeOptionsSerializer, CustomMadePageSerializer,
                          BrandCartSerializer, ProductBrandSerializer, BrandPageSerializer)
from django.shortcuts import get_object_or_404
from math import ceil
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .service import Cart
from django.http import JsonResponse
from datetime import datetime, timedelta
import uuid
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser


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
        product_name = request.query_params.get('product', None)
        product_size = request.query_params.get('size', None)
        product_color = request.query_params.get('color', None)
        compression_class = request.query_params.get('compression_class', None)
        side = request.query_params.get('side', None)

        if product_name and product_size and product_color:
            try:
                product_name = ProductModel.objects.get(product=product_name)
                product_size = SizeProductModel.objects.get(size=product_size)
                product_color = ColorProductModel.objects.get(color=product_color)

                filters = {
                    "product": product_name,
                    "size": product_size,
                    "color": product_color
                }

                if compression_class:
                    filters["compression_class"] = CompressionClassModel.objects.get(compression_class=compression_class)
                if side:
                    filters["side"] = SideModel.objects.get(side=side)

                product_variants = ProductVariantModel.objects.filter(**filters)

                if not product_variants.exists():
                    return Response({"message": "No matching product found"}, status=status.HTTP_404_NOT_FOUND)

                ser_product = ProductVariantShopSerializer(instance=product_variants.first())
                return Response(data=ser_product.data)

            except (ProductModel.DoesNotExist, SizeProductModel.DoesNotExist, ColorProductModel.DoesNotExist,
                    CompressionClassModel.DoesNotExist, SideModel.DoesNotExist):
                return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


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

        if self.request.query_params.get('compression_class'):
            compression_class_query = self.request.query_params.get('compression_class', None)
            compression_class = CompressionClassModel.objects.get(compression_class=compression_class_query)
            products = ProductVariantModel.objects.filter(product=product, color=color,
                                                          compression_class=compression_class, quantity__gt=0)
        else:
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
        # دریافت پارامترهای فیلتر
        page_number = request.query_params.get('page_number', 1)
        limit = request.query_params.get('limit', 15)
        color = request.query_params.get('color', None)
        size = request.query_params.get('size', None)
        gender = request.query_params.get('gender', None)
        category = request.query_params.get('category', None)
        subcategory = request.query_params.get('subcategory', None)
        is_available = request.query_params.get('is_available', None)
        side = request.query_params.get('side', None)
        compression_class = request.query_params.get('compression_class', None)
        brand = request.query_params.get('brand', None)
        
        # دریافت پارامتر مرتب‌سازی
        sort_by = request.query_params.get('sort_by', None)
        
        # بررسی وجود فیلتر
        has_filters = any([color, size, gender, category, subcategory, is_available, side, compression_class, brand])
        
        if has_filters:
            # فیلتر کردن واریانت‌ها
            variant_queryset = ProductVariantModel.objects.all()
            
            if color:
                # تبدیل رشته رنگ‌ها به لیست و حذف فضاهای خالی
                color_list = [c.strip() for c in color.split(',')]
                variant_queryset = variant_queryset.filter(color__color__in=color_list)
            if size:
                # تبدیل رشته سایزها به لیست و حذف فضاهای خالی
                size_list = [s.strip() for s in size.split(',')]
                variant_queryset = variant_queryset.filter(size__size__in=size_list)
            if is_available:
                variant_queryset = variant_queryset.filter(quantity__gt=0)
            if side:
                variant_queryset = variant_queryset.filter(side__side=side)
            if compression_class:
                variant_queryset = variant_queryset.filter(compression_class__compression_class=compression_class)
                
            # استخراج شناسه‌های محصول از واریانت‌های فیلتر شده
            product_ids = variant_queryset.values_list('product_id', flat=True).distinct()
            
            # فیلتر کردن محصولات - فقط محصولات فعال
            queryset = ProductModel.objects.filter(id__in=product_ids, is_active=True).order_by('priority')
            
            if gender:
                if gender.lower() in ["men", "women"]:
                    queryset = queryset.filter(Q(gender__gender__iexact=gender) | Q(gender__gender__iexact="unisex"))
                else:
                    queryset = queryset.filter(gender__gender__iexact=gender)
            if category:
                queryset = queryset.filter(cat_product__category__category__in=category.split(','))
            if subcategory:
                queryset = queryset.filter(sub_product__subcategory__subcategory__in=subcategory.split(','))
            if brand:
                queryset = queryset.filter(brand__brand__in=brand.split(','))
        else:
            # اگر هیچ فیلتری وجود نداشت، فقط محصولات فعال را برگردان
            queryset = ProductModel.objects.filter(is_active=True).order_by('priority')
            
        # محاسبه تعداد کل محصولات فعال (قبل از فیلتر)
        total_all_products = ProductModel.objects.filter(is_active=True).count()
            
        # مرتب‌سازی بر اساس پارامتر sort_by
        if sort_by:
            if sort_by == 'price_high':
                # تبدیل قیمت به عدد اعشاری و مرتب‌سازی نزولی
                queryset = sorted(queryset, key=lambda x: float(x.price.replace(',', '')), reverse=True)
            elif sort_by == 'price_low':
                # تبدیل قیمت به عدد اعشاری و مرتب‌سازی صعودی
                queryset = sorted(queryset, key=lambda x: float(x.price.replace(',', '')))
            elif sort_by == 'newest':
                queryset = queryset.order_by('-created')
            elif sort_by == 'discount_high':
                queryset = queryset.order_by('-percent_discount')
                
        # صفحه‌بندی
        page = int(page_number)
        per_page = int(limit)
        start = (page - 1) * per_page
        end = start + per_page
        
        # محاسبه تعداد کل محصولات فیلتر شده
        if sort_by in ['price_high', 'price_low']:
            total_products = len(queryset)
            products = queryset[start:end]
        else:
            total_products = queryset.count()
            products = queryset[start:end]
            
        total_pages = (total_products + per_page - 1) // per_page
        
        ser_data = ProductAllSerializer(instance=products, many=True, context={'request': request})
        
        return Response({
            'data': ser_data.data,
            'total_pages': total_pages,
            'current_page': page,
            'total_products': total_products,
            'total_all_products': total_all_products  # تعداد کل محصولات فعال قبل از فیلتر
        }, status=status.HTTP_200_OK)


class SearchProductView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all().order_by('priority')
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
        categories = ProductCategoryModel.objects.all().order_by('priority')
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
        subcategories = ProductSubCategoryModel.objects.all().order_by('priority')
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
        try:
            product = ProductModel.objects.get(slug=slug_product)
            ser_data = ProductSerializer(instance=product, context={'request': request})
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


class GetClassView(APIView):
    def get(self, request, slug_product):
        try:
            product = ProductModel.objects.get(slug=slug_product)
            ser_data = GetClassSerializer(instance=product)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


class ProductNewItemView(APIView):
    def get(self, request, slug_product):
        compression_class = self.request.query_params.get('compression_class', None)
        side = self.request.query_params.get('side', None)

        try:
            product = ProductModel.objects.get(slug=slug_product)
            ser_data = NewProductSerializer(instance=product, context={'compression_class': compression_class,
                                                                        'side': side, 'request': request})
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


class FavProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        fav = FavUserModel.objects.get(product=ProductModel.objects.get(id=product_id), user=request.user, fav=True)
        ser_data = FavProductSerializer(instance=fav)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavProductSerializer(data=request.data,
                                          context={'request': request, 'product_id': request.data['product']})
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

        product.fav = False
        product.save()

        return Response(data={'message': f'The fav product ID {product} was deleted'}, status=status.HTTP_200_OK)


class UserFavView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_fav = FavUserModel.objects.filter(user=request.user, fav=True)
        ser_data = UserFavSerializer(instance=product_fav, many=True, context={'request': request})
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CartView(APIView):
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {
                "data": list(cart.__iter__()),
                "cart_total_price": cart.get_total_price(),
                "cart_total_price_without_discount": cart.get_total_price_without_discount(),
                "cart_total_items": cart.__len__()
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)
        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

            response = JsonResponse({"message": 'cart removed', "cart_total_items": cart.__len__()})
            response.delete_cookie('cart_id')
            return response

        elif "clear" in request.data:
            cart.clear()

            response = JsonResponse({"message": 'cart cleaned', "cart_total_items": cart.__len__()})
            response.delete_cookie('cart_id')
            return response

        elif "discount_code" in request.data:
            discount_code = request.data["discount_code"]

            try:
                # پیدا کردن کد تخفیف در دیتابیس
                code = CouponModel.objects.get(coupon_code=discount_code)

                # بررسی معتبر بودن کد
                if code.is_valid() and code.active and (code.limit > 0 or code.infinite):
                    discount_percent = code.discount_percent
                    discount_amount = code.discount_amount
                    data = list(cart.__iter__())
                    total_price = cart.get_total_price()
                    total_price_without_discount = cart.get_total_price_without_discount()

                    # محاسبه قیمت پس از اعمال تخفیف
                    # discounted_price = int(total_price - (total_price * discount_percent / int('100')))
                    discounted_price = int(total_price)
                    if not code.extra_discount and int(code.discount_threshold) <= total_price_without_discount:
                        if discount_percent:
                            discounted_price = int(total_price_without_discount - (total_price_without_discount * int(discount_percent)) / 100)
                        elif discount_amount:
                            discounted_price = int(total_price_without_discount - int(discount_amount))
                    elif code.extra_discount and int(code.discount_threshold) <= total_price:
                        if discount_percent:
                            discounted_price = int(total_price - (total_price * int(discount_percent)) / 100)
                        elif discount_amount:
                            discounted_price = int(total_price - int(discount_amount))
                    else:
                        return JsonResponse(
                            {"message": "The promo code isn't valid. Please verify the code and try again."},
                            status=status.HTTP_400_BAD_REQUEST)

                    # بازگرداندن نتیجه به کاربر
                    return JsonResponse({
                        "message": "Code applied successfully! your total has been updated.",
                        "data": data,
                        "total_price": str(total_price),
                        "discounted_price": str(discounted_price),
                        "cart_total_items": cart.__len__(),
                    })

                else:
                    return JsonResponse({"message": "The promo code isn't valid. Please verify the code and try again."},
                                        status=status.HTTP_400_BAD_REQUEST)

            except CouponModel.DoesNotExist:
                return JsonResponse({"message": "The promo code isn't valid. Please verify the code and try again!"},
                                    status=status.HTTP_400_BAD_REQUEST)

        else:
            product = request.data
            add = cart.add(
                product=product["product"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

            product_variant = ProductVariantModel.objects.get(id=product["product"]["id"])
            item_price = int(product_variant.get_off_price()) * product["quantity"]
            item_price_without_discount = int(product_variant.price) * product["quantity"]
            cart_total_price = sum(int(item["product"]["off_price"]) * item["quantity"] for item in cart)
            response = JsonResponse({"message": add['massage'],
                                     "cart_total_items": cart.__len__(),
                                     "item_total_price": str(item_price),
                                     "item_total_price_without_discount": str(item_price_without_discount),
                                     "cart_total_price": str(cart_total_price),
                                     })
            expires = datetime.now() + timedelta(days=365)  # انقضا پس از 1 سال
            unique_cart_id = str(uuid.uuid4())  # ایجاد یک شناسه تصادفی منحصربه‌فرد

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


class CategoryBestSellerView(APIView):
    def get(self, request):
        categories = ProductCategoryModel.objects.all().order_by('priority')
        ser_data = CategoryBestSellerSerializer(instance=categories, many=True, context={'request': request})
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CustomMadeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {
            'customer_types': CustomerTypeModel.objects.filter(is_enable=True),
            'product_types': ProductTypeModel.objects.filter(is_enable=True),
            'body_areas': BodyAreaModel.objects.filter(is_enable=True),
            'class_numbers': ClassNumberModel.objects.filter(is_enable=True),
            'treatment_categories': TreatmentCategoryModel.objects.filter(is_enable=True),
            'hear_about_us_options': HearAboutUsModel.objects.filter(is_enable=True)
        }
        serializer = CustomMadeOptionsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        files = request.FILES.getlist('attach_file')

        serializer = CustomMadeSerializer(data=data)
        if serializer.is_valid():
            custom_made = serializer.save()

            for file in files:
                CustomMadeAttachFileModel.objects.create(custom_made=custom_made, attach_file=file)

            return Response(
                {
                    "message": "Your custom made request has been submitted successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Invalid data provided",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomMadePageView(APIView):
    def get(self, request):
        custom_made = CustomMadePageModel.objects.all().first()
        ser_data = CustomMadePageSerializer(instance=custom_made)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BrandAllView(APIView):
    def get(self, request):

        brands = ProductBrandModel.objects.all()
        brands_serializer = ProductBrandSerializer(instance=brands, many=True)

        return Response(brands_serializer.data, status=status.HTTP_200_OK)


class BrandPageView(APIView):
    def get(self, request, brand_slug):
        try:
            # Get brand page data
            brand_page = ProductBrandModel.objects.get(slug=brand_slug)
            brand_page_serializer = BrandPageSerializer(instance=brand_page)

            # Get brand cart data
            brand_cart = BrandCartModel.objects.filter(brand=ProductBrandModel.objects.get(slug=brand_slug))
            brand_cart_serializer = BrandCartSerializer(instance=brand_cart, many=True)

            return Response({
                'brand_page': brand_page_serializer.data,
                'brand_cart': brand_cart_serializer.data
            }, status=status.HTTP_200_OK)
        except (ProductBrandModel.DoesNotExist, BrandCartModel.DoesNotExist):
            return Response({'message': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)
