from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import User, RoleModel, RoleUserModel
from .serializers import (UserSerializer, UserValueSerializer, RoleSerializer, LoginUserSerializer, BlogTagSerializer,
                          AddBlogTagSerializer, AddRoleSerializer, BlogCategorySerializer, CombinedBlogSerializer,
                          ExtraGroupSerializer, SizeValueCUDSerializer, SizeValueSerializer, ColorValueCUDSerializer,
                          ColorValueSerializer, ProductTagSerializer, CombinedProductSerializer, GenderSerializer,
                          ProductWithVariantsSerializer, ProductVariantSerializer, OrderSerializer,
                          OrderDetailSerializer, OrderItemSerializer)
from accounts.serializers import UserRegisterSerializer, UserInfoSerializer
from rest_framework import status
from math import ceil
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserLoginSerializer
from blog.serializers import BlogAllSerializer, BlogSerializer, ImageBlogSerializer
from blog.models import BlogModel, BlogTagModel, AddBlogTagModel, BlogCategoryModel
from rest_framework.permissions import IsAuthenticated
from home.models import CommentHomeModel, BannerSliderModel, VideoHomeModel
from home.serializers import CommentHomeSerializer, VideoHomeSerializer, BannerSliderSerializer
from product.models import (ProductCategoryModel, ProductSubCategoryModel, ExtraGroupModel, SizeProductModel,
                            ColorProductModel, ProductModel, ProductTagModel, AddProductTagModel, ProductGenderModel,
                            ProductVariantModel, AddImageGalleryModel)
from product.serializers import (ProductCategorySerializer, ProductSubCategorySerializer, ProductSerializer,
                                 AddProductTagSerializer, ProductColorImageSerializer, ProductAdminSerializer,
                                 ProductColorImageListSerializer)
from collections import defaultdict
from order.models import OrderModel, OrderItemModel


class LanguageView(APIView):
    def get(self, request):
        data = [{
            'id': 1,
            'title': 'English',
            'locale': 'en',
            'backward': 'false',
            'default': 'true',
            'active': 'true'
        }]
        return Response(data={'data': data})


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        ser_data = UserValueSerializer(instance=user)
        return Response(ser_data.data)

    def post(self, request):
        """
                parameters:
                1. first_name
                2. last_name
                3. email
                4. phone_number
                5. trn_number
                6. company_name
                7. password
                """
        form = request.data
        ser_data = UserRegisterSerializer(data=form)
        if ser_data.is_valid():
            user = User.objects.filter(email=form['email']).exists()
            if not user:
                User.objects.create_user(first_name=form['first_name'],
                                         last_name=form['last_name'],
                                         email=form['email'],
                                         phone_number=form['phone_number'],
                                         trn_number=form['trn_number'],
                                         company_name=form['company_name'],
                                         password=form['password']),
                return Response(data={'message': 'user created'},
                                status=status.HTTP_201_CREATED)

            else:
                return Response(data={'message': 'user with this Email already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        """
        parameters:
        1. first_name
        2. last_name
        3. emai
        4. phone_number
        5. company_name
        6. trn_number
        7. zoho_customer_id
        8. is_active
        """
        user = get_object_or_404(User, id=user_id)
        form = request.data

        ser_user_info = UserValueSerializer(instance=user, data=form, partial=True)
        if ser_user_info.is_valid():
            ser_user_info.save()
            return Response(data={'message': 'Done'}, status=status.HTTP_200_OK)
        return Response(data=ser_user_info.errors, status=status.HTTP_400_BAD_REQUEST)


class UserValueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = self.request.query_params.get('page', None)

        per_page = 20
        product_count = len(User.objects.all())
        number_of_pages = ceil(product_count / per_page)

        if page is not None:
            page = int(page)
            product = User.objects.all()[per_page * (page - 1):per_page * page]
        else:
            product = User.objects.all()

        ser_data = UserSerializer(instance=product, many=True)
        return Response({'data': ser_data.data, 'number_of_pages': number_of_pages})


class RoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = RoleModel.objects.all()
        ser_data = RoleSerializer(instance=role, many=True)
        return Response(data=ser_data.data)

    def put(self, request):
        form = request.data

        user = get_object_or_404(User, id=form['user'])
        if RoleUserModel.objects.filter(user=user).exists():
            role_user = get_object_or_404(RoleUserModel, user=user)
            ser_data = AddRoleSerializer(instance=role_user, data=form, partial=True)
            if ser_data.is_valid():
                ser_data.save()
                return Response(data=ser_data.data, status=status.HTTP_200_OK)
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        ser_data = AddRoleSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):

    def post(self, request):
        """
        parameters:
        1. email
        2. password
        """
        form = request.data
        ser_data = UserLoginSerializer(data=form)
        if ser_data.is_valid():
            try:
                user = authenticate(email=form['email'], password=form['password'])
                if user is not None:
                    user = User.objects.get(email=form['email'])
                    if user.is_admin:
                        token_access = AccessToken.for_user(user)
                        token_refresh = RefreshToken.for_user(user)

                        ser_data = LoginUserSerializer(instance=user)

                        return Response(data={'data': {'access_token': str(token_access),
                                                       'refresh_token': str(token_refresh),
                                                       'token_type': 'Bearer',
                                                       'user': ser_data.data}},
                                        status=status.HTTP_200_OK)
                    return Response(data='user is not active', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data='user invalid', status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'message': 'Authenticate Error.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# Blog
class BlogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = BlogModel.objects.all()
        ser_data = BlogAllSerializer(instance=blogs, many=True)
        return Response(data=ser_data.data)


class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        blog = get_object_or_404(BlogModel, id=blog_id)
        ser_data = BlogSerializer(instance=blog)
        return Response(data=ser_data.data)

    def post(self, request, *args, **kwargs):
        serializer = CombinedBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id):
        if blog_id is None:
            return Response(data={'message': 'Input Blog ID'})
        try:
            blog = BlogModel.objects.get(id=blog_id)
        except:
            return Response(data={'message': 'Blog is not exist'})

        ser_data = CombinedBlogSerializer(instance=blog, data=request.data, partial=True)

        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id):
        if blog_id is None:
            return Response(data={'message': 'Input Blog ID'})

        try:
            blog = BlogModel.objects.get(id=blog_id)
        except:
            return Response(data={'message': 'Blog is not exist'})

        blog.delete()

        return Response(data={'message': f'The Blog ID {blog_id} was deleted'})


class BlogCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = BlogCategoryModel.objects.all()
        ser_data = BlogCategorySerializer(instance=category, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BlogCategorySerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        form = request.data
        category = BlogCategoryModel.objects.get(id=category_id)
        ser_data = BlogCategorySerializer(instance=category, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BLogTagListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = self.request.query_params.get('search')
        if search is None:
            blog_tag = BlogTagModel.objects.all()
            ser_data = BlogTagSerializer(instance=blog_tag, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        blog_tag = BlogTagModel.objects.filter(tag__icontains=search)
        ser_data = BlogTagSerializer(instance=blog_tag, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BlogTagSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, tag_id):
        form = request.data
        tag_blog = BlogTagModel.objects.get(id=tag_id)
        ser_data = BlogTagSerializer(instance=tag_blog, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tag_id):
        if tag_id is None:
            return Response(data={'message': 'Input Tag ID'})

        try:
            tag_blog = BlogTagModel.objects.get(id=tag_id)
        except:
            return Response(data={'message': 'Tag is not exist'})

        tag_blog.delete()

        return Response(data={'message': f'The Blog ID {tag_id} was deleted'})


class BLogTagItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tag_id):
        tag = get_object_or_404(BlogTagModel, id=tag_id)
        ser_data = BlogTagSerializer(instance=tag)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class AddBLogTagListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = request.data
        ser_data = AddBlogTagSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id):
        if blog_id is None:
            return Response(data={'message': 'Input Blog ID'})
        try:
            add_tag = AddBlogTagModel.objects.get(blog=blog_id)
        except:
            return Response(data={'message': 'Blog is not exist'})

        ser_data = AddBlogTagSerializer(instance=add_tag, data=request.data, partial=True)

        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id):
        if blog_id is None:
            return Response(data={'message': 'Input Blog ID'})

        try:
            add_tag = AddBlogTagModel.objects.get(blog=blog_id)
        except:
            return Response(data={'message': 'Blog is not exist'})

        add_tag.delete()

        return Response(data={'message': f'The Blog ID {blog_id} was deleted'})


class CommentHomeView(APIView):
    def get(self, request):
        comments = CommentHomeModel.objects.all()
        ser_data = CommentHomeSerializer(instance=comments, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CommentItemView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(CommentHomeModel, id=comment_id)
        ser_data = CommentHomeSerializer(instance=comment)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CommentHomeSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        form = request.data
        comment = get_object_or_404(CommentHomeModel, id=comment_id)
        ser_data = CommentHomeSerializer(instance=comment, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        if comment_id is None:
            return Response(data={'message': 'Input Comment ID'})

        try:
            comment = CommentHomeModel.objects.get(id=comment_id)
        except:
            return Response(data={'message': 'Comment is not exist'})

        comment.delete()

        return Response(data={'message': f'The Comment ID {comment_id} was deleted'})


class BannerHomeView(APIView):
    def get(self, request):
        banner = BannerSliderModel.objects.all()
        ser_data = BannerSliderSerializer(instance=banner, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BannerItemView(APIView):
    def get(self, request, banner_id):
        banner = get_object_or_404(BannerSliderModel, id=banner_id)
        ser_data = BannerSliderSerializer(instance=banner)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BannerSliderSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, banner_id):
        form = request.data
        banner = get_object_or_404(BannerSliderModel, id=banner_id)
        ser_data = BannerSliderSerializer(instance=banner, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, banner_id):
        if banner_id is None:
            return Response(data={'message': 'Input Banner ID'})

        try:
            banner = BannerSliderModel.objects.get(id=banner_id)
        except:
            return Response(data={'message': 'Banner is not exist'})

        banner.delete()

        return Response(data={'message': f'The Banner ID {banner_id} was deleted'})


class VideoHomeView(APIView):
    def get(self, request):
        video = VideoHomeModel.objects.all()
        ser_data = VideoHomeSerializer(instance=video, many=True)
        return Response(data=ser_data.data)

    def put(self, request, video_id):
        form = request.data
        video = get_object_or_404(VideoHomeModel, id=video_id)
        ser_data = VideoHomeSerializer(instance=video, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryView(APIView):

    def get(self, request):
        category = ProductCategoryModel.objects.all()
        ser_data = ProductCategorySerializer(instance=category, many=True)

        return Response(data=ser_data.data)


class ProductCategoryItemView(APIView):
    def get(self, request, category_id):
        category = get_object_or_404(ProductCategoryModel, id=category_id)
        ser_data = ProductCategorySerializer(instance=category)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ProductCategorySerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        form = request.data
        category = get_object_or_404(ProductCategoryModel, id=category_id)
        ser_data = ProductCategorySerializer(instance=category, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        if category_id is None:
            return Response(data={'message': 'Input Category ID'})

        try:
            category = ProductCategoryModel.objects.get(id=category_id)
        except:
            return Response(data={'message': 'Category is not exist'})

        category.delete()

        return Response(data={'message': f'The Category ID {category_id} was deleted'})


class ProductSubCategoryView(APIView):

    def get(self, request):
        subcategory = ProductSubCategoryModel.objects.all()
        ser_data = ProductSubCategorySerializer(instance=subcategory, many=True)

        return Response(data=ser_data.data)


class ProductSubCategoryItemView(APIView):
    def get(self, request, category_id):
        subcategory = get_object_or_404(ProductSubCategoryModel, id=category_id)
        ser_data = ProductSubCategorySerializer(instance=subcategory)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ProductSubCategorySerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        form = request.data
        subcategory = get_object_or_404(ProductSubCategoryModel, id=category_id)
        ser_data = ProductSubCategorySerializer(instance=subcategory, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        if category_id is None:
            return Response(data={'message': 'Input Category ID'})

        try:
            subcategory = ProductSubCategoryModel.objects.get(id=category_id)
        except:
            return Response(data={'message': 'Category is not exist'})

        subcategory.delete()

        return Response(data={'message': f'The Category ID {category_id} was deleted'})


class BlogImageView(APIView):
    def post(self, request):
        form = request.data
        ser_data = ImageBlogSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            response = {'data': {
                'title': ser_data.data['image'], 'type': ser_data.data['type']}
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtraItemView(APIView):
    def get(self, request):
        extr_group = ExtraGroupModel.objects.all()
        ser_data = ExtraGroupSerializer(instance=extr_group, many=True)
        return Response(data=ser_data.data)


class ExtraGroupView(APIView):
    def get(self, request, id_extrag):
        extra = get_object_or_404(ExtraGroupModel, id=id_extrag)
        ser_data = ExtraGroupSerializer(instance=extra)
        return Response(data=ser_data.data)

    def post(self, request):
        form = request.data

        ser_data = ExtraGroupSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_extrag):
        if id_extrag is None:
            return Response(data={'message': 'Input Extra Group ID'})

        try:
            extrag = ExtraGroupModel.objects.get(id=id_extrag)
        except:
            return Response(data={'message': 'Extra Group is not exist'})

        ser_data = ExtraGroupSerializer(instance=extrag, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_extrag):
        if id_extrag is None:
            return Response(data={'message': 'Input Extra Group ID'})

        try:
            extrag = ExtraGroupModel.objects.get(id=id_extrag)
        except:
            return Response(data={'message': 'Extra Group is not exist'})

        name = extrag.title
        extrag.delete()
        return Response(data={'message': f'The {name} Extra Group was deleted'})


class SizeItemView(APIView):
    def get(self, request, size_id):

        size = get_object_or_404(SizeProductModel, id=size_id)
        ser_data = SizeValueSerializer(instance=size)
        return Response(data=ser_data.data)


class SizeValueView(APIView):
    def get(self, request):

        size = SizeProductModel.objects.all()
        ser_data = SizeValueSerializer(instance=size, many=True)
        return Response(data=ser_data.data)

    def post(self, request):
        form = request.data

        ser_data = SizeValueCUDSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_size):
        # id_size = request.data['id_size']

        if id_size is None:
            return Response(data={'message': 'Input Size ID'})

        try:
            size = SizeProductModel.objects.get(id=id_size)
        except:
            return Response(data={'message': 'Size is not exist'})

        ser_data = SizeValueCUDSerializer(instance=size, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_size):
        if id_size is None:
            return Response(data={'message': 'Input Size ID'})

        try:
            size = SizeProductModel.objects.get(id=id_size)
        except:
            return Response(data={'message': 'Size is not exist'})

        name = size.size
        size.delete()
        return Response(data={'message': f'The {name} Size was deleted'})


class ColorItemView(APIView):
    def get(self, request, color_id):

        color = get_object_or_404(ColorProductModel, id=color_id)
        ser_data = ColorValueSerializer(instance=color)
        return Response(data=ser_data.data)


class ColorValueView(APIView):
    def get(self, request):

        color = ColorProductModel.objects.all()
        ser_data = ColorValueSerializer(instance=color, many=True)
        return Response(data=ser_data.data)

    def post(self, request):
        form = request.data

        ser_data = ColorValueCUDSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_color):
        # id_color = request.data['id_color']

        if id_color is None:
            return Response(data={'message': 'Input Color ID'})

        try:
            size = ColorProductModel.objects.get(id=id_color)
        except:
            return Response(data={'message': 'Color is not exist'})

        ser_data = ColorValueCUDSerializer(instance=size, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_color):

        if id_color is None:
            return Response(data={'message': 'Input Color ID'})

        try:
            color = ColorProductModel.objects.get(id=id_color)
        except:
            return Response(data={'message': 'Color is not exist'})

        name = color.color
        color.delete()
        return Response(data={'message': f'The {name} Color was deleted'})


class ProductView(APIView):
    def get(self, request):
        products = ProductModel.objects.all()
        ser_data = ProductSerializer(instance=products, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
        # per_page = int(self.request.query_params.get('limit', 10))
        # page = self.request.query_params.get('page', None)
        #
        # product_count = len(ProductModel.objects.all())
        # number_of_pages = ceil(product_count / per_page)
        #
        # if page is not None:
        #     page = int(page)
        #     product = ProductModel.objects.all()[per_page*(page-1):per_page*page]
        # else:
        #     product = ProductModel.objects.all()
        #
        # ser_data = ProductSerializer(instance=product, many=True)
        # return Response({'data': ser_data.data, 'number_of_pages': number_of_pages})


class ProductItemView(APIView):
    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        ser_data = ProductSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CombinedProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        print(product)
        serializer = CombinedProductSerializer(instance=product, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            print('-'*100)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):

        if product_id is None:
            return Response(data={'message': 'Input Product ID'})

        try:
            product = ProductModel.objects.get(id=product_id)
        except:
            return Response(data={'message': 'Product is not exist'})

        name = product.product
        product.delete()
        return Response(data={'message': f'The {name} Product was deleted'})


class ProductTagListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        search = self.request.query_params.get('search')
        if search is None:
            product_tag = ProductTagModel.objects.all()
            ser_data = ProductTagSerializer(instance=product_tag, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        product_tag = ProductTagModel.objects.filter(tag__icontains=search)
        ser_data = ProductTagSerializer(instance=product_tag, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ProductTagSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        form = request.data
        product_tag = ProductTagModel.objects.get(id=product_id)
        ser_data = ProductTagSerializer(instance=product_tag, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        if product_id is None:
            return Response(data={'message': 'Input Tag ID'})

        try:
            tag_product = ProductTagModel.objects.get(id=product_id)
        except:
            return Response(data={'message': 'Tag is not exist'})

        tag_product.delete()

        return Response(data={'message': f'The Product ID {product_id} was deleted'})


class ProductTagItemView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(ProductTagModel, id=product_id)
        ser_data = ProductTagSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class AddProductTagListView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        form = request.data
        ser_data = AddProductTagSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response(data={'message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            add_tag = AddProductTagModel.objects.get(product=product)
        except AddProductTagModel.DoesNotExist:
            return Response(data={'message': 'Product tag does not exist'}, status=status.HTTP_404_NOT_FOUND)

        ser_data = AddProductTagSerializer(instance=add_tag, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        if product_id is None:
            return Response(data={'message': 'Input Product ID'})

        try:
            add_tag = AddProductTagModel.objects.get(product=product_id)
        except:
            return Response(data={'message': 'Product is not exist'})

        add_tag.delete()

        return Response(data={'message': f'The Product ID {product_id} was deleted'})


class GenderView(APIView):
    def get(self, request):
        genders = ProductGenderModel.objects.all()
        ser_data = GenderSerializer(instance=genders, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = GenderSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class GenderItemView(APIView):
    def put(self, request, gender_id):
        try:
            gender = ProductGenderModel.objects.get(id=gender_id)
        except ProductModel.DoesNotExist:
            return Response(data={'message': 'Gender does not exist'}, status=status.HTTP_404_NOT_FOUND)

        ser_data = GenderSerializer(instance=gender, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, gender_id):
        if gender_id is None:
            return Response(data={'message': 'Input Gender ID'})

        try:
            gender = ProductGenderModel.objects.get(id=gender_id)
        except:
            return Response(data={'message': 'Gender is not exist'})

        gender.delete()

        return Response(data={'message': f'The Gender ID {gender_id} was deleted'}, status=status.HTTP_200_OK)


class ProductVariantView(APIView):
    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        variant = ProductVariantModel.objects.filter(product=product)
        ser_data = ProductVariantSerializer(instance=variant, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        # print(form.getlist('extras'))
        # print(type(form))
        ser_data = ProductWithVariantsSerializer(data=request.data)

        if ser_data.is_valid():

            extras = ser_data.validated_data['extras']
            for extra in extras:
                ProductVariantModel.objects.create(product=ProductModel.objects.get(id=product_id),
                                                   name=extra['name'],
                                                   item_id=extra['item_id'],
                                                   color=extra['color'],
                                                   size=extra['size'],
                                                   price=extra['price'],
                                                   percent_discount=extra['percent_discount'],
                                                   quantity=extra['quantity'],
                                                   )

            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class VariantPutView(APIView):
    def put(self, request):
        ser_data = ProductWithVariantsSerializer(data=request.data)
        print(ser_data)
        if ser_data.is_valid():

            extras = ser_data.validated_data['extras']
            print(extras)
            for extra in extras:
                print(extra)
                variant = ProductVariantModel.objects.get(id=(extra['id']))
                print('-'*100)
                if variant:
                    variant.name = extra['name']
                    variant.item_id = extra['item_id']
                    variant.color_id = extra['color']  # Assigning the ID directly
                    variant.size_id = extra['size']  # Assigning the ID directly
                    variant.price = extra['price']
                    variant.percent_discount = extra['percent_discount']
                    variant.quantity = extra['quantity']
                    variant.save()
                print('*'*100)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageGallery(APIView):
    def post(self, request):
        query_dict = dict(request.data)
        data = defaultdict(dict)
        print(query_dict)
        print('-' * 100)

        for key, value in query_dict.items():
            # Split the key into parts
            parts = key.split('.')
            print(parts)
            index = int(parts[1])
            field = parts[2]

            # Assign the value to the appropriate place in the dictionary
            if field in ['product', 'color']:
                # Convert the value to an integer
                data[index][field] = int(value[0])
            else:
                # Handle images or other types of data
                data[index][field] = value[0] if isinstance(value, list) else value

        # Convert defaultdict to a list of dictionaries
        data_list = [data[i] for i in sorted(data.keys())]
        print(data_list)

        if not data_list:
            return Response({"error": "No data found in request"}, status=status.HTTP_400_BAD_REQUEST)

        for form_data in data_list:
            ser_data = ProductColorImageSerializer(data=form_data)
            if ser_data.is_valid():
                ser_data.save()
            else:
                return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Done', status=status.HTTP_201_CREATED)


        # AddImageGalleryModel.objects.filter(product_id=product_id).delete()
        # print('-'*100)
        # for form_data in data_list:
        #     print('#' * 100)
        #     ser_data = ProductColorImageSerializer(data=form_data)
        #     if ser_data.is_valid():
        #         print('!' * 100)
        #         ser_data.save()
        #         print('?' * 100)
        #     else:
        #         print('*' * 100)
        #         return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # return Response(data='Done', status=status.HTTP_201_CREATED)
    def put(self, request):
        query_dict = dict(request.data)
        data = defaultdict(dict)

        for key, value in query_dict.items():
            # Split the key into parts
            parts = key.split('.')
            index = int(parts[1])
            field = parts[2]

            # Assign the value to the appropriate place in the dictionary
            if field in ['product', 'color']:
                # Convert the value to an integer
                data[index][field] = int(value[0])
            else:
                # Handle images or other types of data
                data[index][field] = value[0] if isinstance(value, list) else value

        # Convert defaultdict to a list of dictionaries
        images_data = [data[i] for i in sorted(data.keys())]

        if not images_data:
            return Response({"error": "No data found in request"}, status=status.HTTP_400_BAD_REQUEST)
        results = []
        print(images_data)
        for data in images_data:
            product = data.get('product')
            color = data.get('color')
            image = data.get('image')

            # استفاده از `update_or_create` برای مدیریت تصاویر
            obj, created = AddImageGalleryModel.objects.update_or_create(
                product_id=product,
                color_id=color,
                defaults={'image': image},
            )

            results.append(ProductColorImageSerializer(obj).data)

        return Response(results, status=status.HTTP_200_OK)


class VariantDataView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        ser_data = ProductAdminSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class VariantImageView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        gallery = AddImageGalleryModel.objects.filter(product=product)
        ser_data = ProductColorImageSerializer(instance=gallery, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ColorImageView(APIView):
    def post(self, request, product_id):

        product = ProductModel.objects.get(id=product_id)
        sizes = request.data['sizes']
        colors = request.data['colors']
        for color in colors:
            for size in sizes:
                if not ProductVariantModel.objects.filter(product=product,
                                                          color=ColorProductModel.objects.get(color=color),
                                                          size=SizeProductModel.objects.get(size=size),
                                                          ).exists():
                    ProductVariantModel.objects.create(product=product,
                                                       color=ColorProductModel.objects.get(color=color),
                                                       size=SizeProductModel.objects.get(size=size),
                                                       price=0,
                                                       quantity=0,
                                                       name=f'{product}-{color}-{size}')
        return Response(data={'message': 'Create'}, status=status.HTTP_201_CREATED)


class OrderPaidView(APIView):
    def get(self, request):
        order = OrderModel.objects.filter(paid=True)
        ser_data = OrderSerializer(instance=order, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderUnpaidView(APIView):
    def get(self, request):
        order = OrderModel.objects.filter(paid=False)
        ser_data = OrderSerializer(instance=order, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = OrderModel.objects.get(id=order_id)
        ser_data = OrderDetailSerializer(instance=order)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        try:
            order = OrderModel.objects.get(id=order_id)
        except ProductModel.DoesNotExist:
            return Response(data={'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

        ser_data = OrderDetailSerializer(instance=order, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCustomerView(APIView):
    def get(self, request, order_id):
        user = OrderModel.objects.get(id=order_id).user
        ser_data = UserInfoSerializer(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderItemsView(APIView):
    def get(self, request, order_id):
        items = OrderItemModel.objects.filter(order=order_id)
        ser_data = OrderItemSerializer(instance=items, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

# class VideoItemView(APIView):
#     def get(self, request, video_id):
#         video = get_object_or_404(VideoHomeModel, id=video_id)
#         ser_data = VideoHomeSerializer(instance=video)
#         return Response(data=ser_data.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         form = request.data
#         ser_data = VideoHomeSerializer(data=form)
#         if ser_data.is_valid():
#             ser_data.save()
#             return Response(data=ser_data.data, status=status.HTTP_200_OK)
#         return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, video_id):
#         form = request.data
#         video = get_object_or_404(VideoHomeModel, id=video_id)
#         ser_data = VideoHomeSerializer(instance=video, data=form, partial=True)
#         if ser_data.is_valid():
#             ser_data.save()
#             return Response(data=ser_data.data, status=status.HTTP_200_OK)
#         return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
