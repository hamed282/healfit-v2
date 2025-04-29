from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import User, RoleModel, RoleUserModel
from .serializers import (UserSerializer, UserValueSerializer, RoleSerializer, LoginUserSerializer, BlogTagSerializer,
                          AddBlogTagSerializer, AddRoleSerializer, BlogCategorySerializer, CombinedBlogSerializer,
                          ExtraGroupSerializer, SizeValueCUDSerializer, SizeValueSerializer, ColorValueCUDSerializer,
                          ColorValueSerializer, ProductTagSerializer, CombinedProductSerializer, GenderSerializer,
                          ProductWithVariantsSerializer, ProductVariantSerializer, OrderSerializer,
                          OrderDetailSerializer, OrderItemSerializer, ChangePasswordSerializer, CommentBlogSerializer,
                          ShippingCountrySerializer, ShippingSerializer, CityShippingSerializer, BlogAuthorSerializer,
                          CustomerTypeSerializer, ProductTypeSerializer, BodyAreaSerializer, HearAboutUsSerializer,
                          TreatmentCategorySerializer, ClassNumberSerializer, CompressionClassSerializer,
                          SideSerializer, BrandSerializer, ProductSerializer)
from accounts.serializers import UserRegisterSerializer, UserInfoSerializer
from rest_framework import status
from math import ceil
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserLoginSerializer
from blog.serializers import BlogAllSerializer, BlogSerializer, ImageBlogSerializer
from blog.models import BlogModel, BlogTagModel, AddBlogTagModel, BlogCategoryModel, CommentBlogModel, AuthorBlogModel
from rest_framework.permissions import IsAdminUser
from home.models import (CommentHomeModel, BannerSliderModel, VideoHomeModel, BannerShopModel,
                         SEOHomeModel, LogoModel, NewsLetterModel, ContactSubmitModel, AboutPageModel, CareerPageModel,
                         BlogPageModel, ShopPageModel, SitemapPageModel, WholesaleInquiryPageModel,
                         CustomerCarePageModel, RefundPolicyPageModel, ContactUsPageModel, BannerSliderMobileModel,
                         Content1Model, Content2Model, Content3Model)
from home.serializers import (CommentHomeSerializer, VideoHomeSerializer, BannerSliderSerializer,
                              BannerShopSerializer, LogoHomeSerializer, SEOHomeSerializer, NewsLetterSerializer,
                              ContactSubmitSerializer, AboutPageSerializer, ShopPageSerializer, BlogPageSerializer,
                              CareerPageSerializer, SitemapPageSerializer, ContactUsPageSerializer,
                              RefundPolicyPageSerializer, WholesaleInquiryPageSerializer, CustomerCarePageSerializer,
                              BannerSliderMobileSerializer, ContentHome1Serializer)
from product.models import (ProductCategoryModel, ProductSubCategoryModel, ExtraGroupModel, SizeProductModel,
                            ColorProductModel, ProductModel, ProductTagModel, AddProductTagModel, ProductGenderModel,
                            ProductVariantModel, AddImageGalleryModel, CouponModel, CustomMadeModel, CustomerTypeModel,
                            ProductTypeModel, BodyAreaModel, HearAboutUsModel, TreatmentCategoryModel, ClassNumberModel,
                            CompressionClassModel, SideModel, ProductBrandModel)
from product.serializers import (ProductCategorySerializer, ProductSubCategorySerializer,
                                 AddProductTagSerializer, ProductColorImageSerializer, ProductAdminSerializer,
                                 CouponSerializer, CouponCreateSerializer, CustomMadeSerializer)
from collections import defaultdict
from order.models import OrderModel, OrderItemModel, OrderStatusModel, ShippingModel, ShippingCountryModel
from django.db.models import Subquery
from permissions import (IsBlogAdmin, IsProductAdmin, IsOrderAdmin, IsModeratorAdmin, IsSEOAdmin, IsAccountAdmin,
                         IsSuperAdmin, OrPermission)
from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.http import JsonResponse
from django.core.management import call_command


# Account Section
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
    permission_classes = [IsAdminUser, IsAccountAdmin]

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
                8. role
                """
        form = request.data
        ser_data = UserRegisterSerializer(data=form)
        if ser_data.is_valid():
            user = User.objects.filter(email=form['email']).exists()
            if not user:
                new_user = User.objects.create_user(first_name=form['first_name'],
                                                    last_name=form['last_name'],
                                                    email=form['email'],
                                                    phone_number=form['phone_number'],
                                                    trn_number=form['trn_number'],
                                                    company_name=form['company_name'],
                                                    is_active=form['is_active'],
                                                    is_admin=form['is_admin'],
                                                    password=form['password'])
                RoleUserModel.objects.create(user=new_user, role=RoleModel.objects.get(role=form['role']))
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
        9. role
        """
        user = get_object_or_404(User, id=user_id)
        form = request.data

        ser_user_info = UserValueSerializer(instance=user, data=form, partial=True)
        if ser_user_info.is_valid():
            ser_user_info.save()

            if 'role' in form:
                try:
                    role_user = RoleUserModel.objects.get(user=user)
                    role_user.role = RoleModel.objects.get(role=form['role'])
                    role_user.save()
                except:
                    RoleUserModel.objects.create(user=user, role=RoleModel.objects.get(role=form['role']))

            return Response(data={'message': 'Done'}, status=status.HTTP_200_OK)
        return Response(data=ser_user_info.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAdminUser, IsAccountAdmin]

    @staticmethod
    def post(request, user_id):
        """
        parameters:
        2. new_password
        """
        ser_data = ChangePasswordSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(ser_data.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user)  # To update session after password change
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleUpdateView(APIView):
    # permission_classes = [IsAdminUser, IsAccountAdmin]

    def put(self, request, user_id):
        user = User.objects.get(id=user_id)
        role = RoleModel.objects.get(role=request.data['role'])

        if RoleUserModel.objects.filter(user=user).exists():
            role_user = RoleUserModel.objects.get(user=user)
            role_user.role = role
            role_user.save()
        else:
            RoleUserModel.objects.create(user=user, role=role)

        return Response(data={'message': 'User role Updated'})


class UserValueView(APIView):
    permission_classes = [IsAdminUser, IsAccountAdmin]

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
        return Response({'data': ser_data.data})


class RoleView(APIView):
    permission_classes = [IsAdminUser, IsAccountAdmin]

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


# Blog Section
class BlogListView(APIView):
    permission_classes = [IsAdminUser, IsBlogAdmin | IsSEOAdmin]

    def get(self, request):
        blogs = BlogModel.objects.all()
        ser_data = BlogAllSerializer(instance=blogs, many=True)
        return Response(data=ser_data.data)


class BlogView(APIView):
    permission_classes = [IsAdminUser, IsBlogAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsBlogAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsBlogAdmin | IsSEOAdmin]

    def get(self, request):
        search = self.request.query_params.get('search')

        used_tags = AddBlogTagModel.objects.values('tag')

        if search is None:
            blog_tag = BlogTagModel.objects.exclude(id__in=Subquery(used_tags))
        else:
            blog_tag = BlogTagModel.objects.filter(tag__icontains=search).exclude(id__in=Subquery(used_tags))

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
    permission_classes = [IsAdminUser, IsBlogAdmin | IsSEOAdmin]

    def get(self, request, tag_id):
        tag = get_object_or_404(BlogTagModel, id=tag_id)
        ser_data = BlogTagSerializer(instance=tag)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class AddBLogTagListView(APIView):
    permission_classes = [IsAdminUser, IsBlogAdmin | IsSEOAdmin]

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


class BlogImageView(APIView):
    # permission_classes = [IsAdminUser, IsBlogAdmin | IsSEOAdmin]

    def post(self, request):
        def remove_after_question_mark(text):
            index = text.find('?')
            if index != -1:
                return text[:index]
            return text

        form = request.data
        ser_data = ImageBlogSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            response = {'data': {
                'title': remove_after_question_mark(ser_data.data['image']), 'type': ser_data.data['type']}
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogCommentsView(APIView):
    def get(self, request):
        comments = CommentBlogModel.objects.all()
        comments.update(new_comment=False)
        ser_data = CommentBlogSerializer(instance=comments, many=True)

        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BlogCommentEditView(APIView):
    def put(self, request, comment_id):
        comment = CommentBlogModel.objects.get(id=comment_id)
        ser_data = CommentBlogSerializer(instance=comment, partial=True, data=request.data)
        if ser_data.is_valid():
            ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BlogCommentsNotifView(APIView):
    def get(self, request):
        new_comments = CommentBlogModel.objects.filter(new_comment=True).count()
        return Response(data={'new_comments': new_comments})


class SearchBlogCommentView(viewsets.ModelViewSet):
    queryset = CommentBlogModel.objects.all()
    serializer_class = CommentBlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = '__all__'


# Home Section
class CommentHomeView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin | IsSEOAdmin]

    def get(self, request):
        comments = CommentHomeModel.objects.all()
        ser_data = CommentHomeSerializer(instance=comments, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CommentItemView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin]

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
    permission_classes = [IsAdminUser, IsModeratorAdmin | IsSEOAdmin]

    def get(self, request):
        banner = BannerSliderModel.objects.all()
        ser_data = BannerSliderSerializer(instance=banner, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BannerMobileHomeView(APIView):
    # permission_classes = [IsAdminUser, IsModeratorAdmin | IsSEOAdmin]

    def get(self, request):
        banner = BannerSliderMobileModel.objects.all()
        ser_data = BannerSliderSerializer(instance=banner, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BannerItemView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

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


class BannerMobileItemView(APIView):
    # permission_classes = [IsAdminUser, IsModeratorAdmin]

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'GET']:
    #         return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
    #     return super().get_permissions()

    def get(self, request, banner_id):
        banner = get_object_or_404(BannerSliderMobileModel, id=banner_id)
        ser_data = BannerSliderSerializer(instance=banner)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BannerSliderMobileSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, banner_id):
        form = request.data
        banner = get_object_or_404(BannerSliderMobileModel, id=banner_id)
        ser_data = BannerSliderMobileSerializer(instance=banner, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, banner_id):
        if banner_id is None:
            return Response(data={'message': 'Input Banner ID'})

        try:
            banner = BannerSliderMobileModel.objects.get(id=banner_id)
        except:
            return Response(data={'message': 'Banner is not exist'})

        banner.delete()

        return Response(data={'message': f'The Banner ID {banner_id} was deleted'})


class VideoHomeView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin |IsSEOAdmin]

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


class HomeContentView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin, IsSEOAdmin]

    def get(self, request):
        content = ContentHomeModel.objects.all()
        ser_data = ContentHomeSerializer(instance=content, many=True)
        return Response(data=ser_data.data)

    def put(self, request, content_id):
        form = request.data
        content = get_object_or_404(ContentHomeModel, id=content_id)
        ser_data = ContentHomeSerializer(instance=content, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerShopView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin | IsSEOAdmin]

    def get(self, request):
        banner = BannerShopModel.objects.all()[:3]
        ser_data = BannerShopSerializer(instance=banner, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BannerShopSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerShopItemView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def get(self, request, banner_id):
        banner = BannerShopModel.objects.get(id=banner_id)
        ser_data = BannerShopSerializer(instance=banner)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, banner_id):
        form = request.data
        banner = get_object_or_404(BannerShopModel, id=banner_id)
        ser_data = BannerShopSerializer(instance=banner, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, banner_id):
        if banner_id is None:
            return Response(data={'message': 'Input Banner ID'})

        try:
            banner = BannerShopModel.objects.get(id=banner_id)
        except:
            return Response(data={'message': 'Banner is not exist'})

        banner.delete()

        return Response(data={'message': f'The Banner ID {banner_id} was deleted'})


class LogoHomeView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin |IsSEOAdmin]

    def get(self, request):
        logo = LogoModel.objects.all()
        ser_data = LogoHomeSerializer(instance=logo, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, logo_id):
        form = request.data
        logo = get_object_or_404(LogoModel, id=logo_id)
        ser_data = LogoHomeSerializer(instance=logo, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SEOHomeView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin | IsSEOAdmin]

    def get(self, request):
        seo = SEOHomeModel.objects.all()
        ser_data = SEOHomeSerializer(instance=seo, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, seo_id):
        form = request.data
        seo = get_object_or_404(SEOHomeModel, id=seo_id)
        ser_data = SEOHomeSerializer(instance=seo, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsLetterView(APIView):
    permission_classes = [IsAdminUser, IsModeratorAdmin]

    def get(self, request):
        newsletter = NewsLetterModel.objects.all()
        ser_data = NewsLetterSerializer(instance=newsletter, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data

        ser_data = NewsLetterSerializer(data=form)

        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, newsletter_id):
        form = request.data
        newsletter = get_object_or_404(NewsLetterModel, id=newsletter_id)
        ser_data = NewsLetterSerializer(instance=newsletter, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# Product Section
class ProductCategoryView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request):
        category = ProductCategoryModel.objects.all()
        ser_data = ProductCategorySerializer(instance=category, many=True)

        return Response(data=ser_data.data)


class ProductCategoryItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request):
        subcategory = ProductSubCategoryModel.objects.all()
        ser_data = ProductSubCategorySerializer(instance=subcategory, many=True)

        return Response(data=ser_data.data)


class ProductSubCategoryItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

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


class ExtraItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request):
        extr_group = ExtraGroupModel.objects.all()
        ser_data = ExtraGroupSerializer(instance=extr_group, many=True)
        return Response(data=ser_data.data)


class ExtraGroupView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request, size_id):

        size = get_object_or_404(SizeProductModel, id=size_id)
        ser_data = SizeValueSerializer(instance=size)
        return Response(data=ser_data.data)


class SizeValueView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request, color_id):

        color = get_object_or_404(ColorProductModel, id=color_id)
        ser_data = ColorValueSerializer(instance=color)
        return Response(data=ser_data.data)


class ColorValueView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()
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
    # permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request):
        products = ProductModel.objects.all()
        ser_data = ProductSerializer(instance=products, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ProductItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        ser_data = ProductSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        form = request.data.copy()

        if 'video' in form and form['video'] in [None, 'null']:
            form.pop('video')
        serializer = CombinedProductSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        form = request.data.copy()

        if 'video' in form and form['video'] in [None, 'null']:
            product.video = None
            product.save()
            form.pop('video')

        serializer = CombinedProductSerializer(instance=product, data=form, partial=True,
                                               context={'product_id': product_id})

        if serializer.is_valid():
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
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request):
        search = self.request.query_params.get('search')

        used_tags = AddProductTagModel.objects.values('tag')

        if search is None:
            product_tag = ProductTagModel.objects.exclude(id__in=Subquery(used_tags))
        else:
            product_tag = ProductTagModel.objects.filter(tag__icontains=search).exclude(id__in=Subquery(used_tags))

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
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request, product_id):
        product = get_object_or_404(ProductTagModel, id=product_id)
        ser_data = ProductTagSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class AddProductTagListView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

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
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

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
    permission_classes = [IsAdminUser, IsProductAdmin]

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
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        variant = ProductVariantModel.objects.filter(product=product)
        ser_data = ProductVariantSerializer(instance=variant, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        ser_data = ProductWithVariantsSerializer(data=request.data)
        product = ProductModel.objects.get(id=product_id)
        if ser_data.is_valid():

            extras = ser_data.validated_data['extras']
            for extra in extras:
                ProductVariantModel.objects.create(product=product,
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
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT']:
            return [OrPermission(IsProductAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def put(self, request):
        ser_data = ProductWithVariantsSerializer(data=request.data)
        if ser_data.is_valid():

            extras = ser_data.validated_data['extras']
            for extra in extras:
                variant = ProductVariantModel.objects.get(id=(extra['id']))
                if variant:
                    variant.name = extra['name']
                    variant.item_id = extra['item_id']
                    variant.color_id = extra['color']  # Assigning the ID directly
                    variant.size_id = extra['size']  # Assigning the ID directly
                    variant.price = extra['price']
                    variant.side = extra['side']
                    variant.compression_class = extra['compression_class']
                    variant.percent_discount = extra['percent_discount']
                    variant.quantity = extra['quantity']
                    variant.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageGallery(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def post(self, request):
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
        data_list = [data[i] for i in sorted(data.keys())]

        if not data_list:
            return Response({"error": "No data found in request"}, status=status.HTTP_400_BAD_REQUEST)

        for form_data in data_list:
            ser_data = ProductColorImageSerializer(data=form_data)
            if ser_data.is_valid():
                ser_data.save()
            else:
                return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Done', status=status.HTTP_201_CREATED)

    def put(self, request):
        query_dict = dict(request.data)
        data = defaultdict(dict)

        for key, value in query_dict.items():
            # Split the key into parts
            parts = key.split('.')
            index = int(parts[1])
            field = parts[2]

            # Assign the value to the appropriate place in the dictionary
            if field in ['product', 'color', 'id']:
                # Convert the value to an integer
                data[index][field] = int(value[0])
            else:
                # Handle images or other types of data
                data[index][field] = value[0] if isinstance(value, list) else value

        # Convert defaultdict to a list of dictionaries
        images_data = [data[i] for i in sorted(data.keys())]

        if not images_data:
            return Response({"error": "No data found in request"}, status=status.HTTP_400_BAD_REQUEST)
        id_gallery_list = []
        for data in images_data:
            id_gallery = data.get('id')
            product_id = data.get('product')
            color = data.get('color')
            image = data.get('image')

            if id_gallery == 0:
                new_gallery = AddImageGalleryModel.objects.create(product=ProductModel.objects.get(id=product_id),
                                                                  color=ColorProductModel.objects.get(id=color),
                                                                  image=image)
                id_gallery_list.append(new_gallery.id)
            else:
                id_gallery_list.append(id_gallery)
        gallery = AddImageGalleryModel.objects.filter(product_id=product_id).exclude(id__in=id_gallery_list)
        gallery.delete()

        return Response(data={'message': 'Done'}, status=status.HTTP_200_OK)


class VariantDataView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        ser_data = ProductAdminSerializer(instance=product)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class VariantImageView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin | IsSEOAdmin]

    def get(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        gallery = AddImageGalleryModel.objects.filter(product=product)
        ser_data = ProductColorImageSerializer(instance=gallery, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ColorImageView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        variants = ProductVariantModel.objects.filter(product=product)

        colors = set([f'{str(p.color.color)} - {str(p.color.color_code)} - {str(p.color.id)}' for p in variants])
        all_colors = [{'color': color.split(" - ")[0], 'code': color.split(" - ")[1], 'id': color.split(" - ")[2]} for
                      color in colors]

        return Response(data=all_colors, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        sizes = request.data['sizes']
        colors = request.data['colors']

        sides = request.data['side']
        # if sides:
        #     sides = SideModel.objects.filter(side=sides)
        # else:
        #     sides = None

        compression_classes = request.data['compression_class']
        # if compression_classes:
        #     compression_classes = CompressionClassModel.objects.filter(compression_class=compression_classes)
        # else:
        #     compression_classes = None
        # print(sides)
        # print(compression_classes)
        for color in colors:
            for size in sizes:
                if sides:
                    for side in sides:
                        side = SideModel.objects.get(side=side)
                        if not ProductVariantModel.objects.filter(product=product,
                                                                  color=ColorProductModel.objects.get(color=color),
                                                                  size=SizeProductModel.objects.get(size=size),
                                                                  side=side
                                                                  ).exists():
                            ProductVariantModel.objects.create(product=product,
                                                               color=ColorProductModel.objects.get(color=color),
                                                               size=SizeProductModel.objects.get(size=size),
                                                               side=side,
                                                               compression_class=None,
                                                               price=0,
                                                               percent_discount=product.percent_discount,
                                                               quantity=0,
                                                               name=f'{product}-{color}-{size}-{side}')
                if compression_classes:
                    for compression_class in compression_classes:
                        compression_class = CompressionClassModel.objects.get(compression_class=compression_class)

                        if not ProductVariantModel.objects.filter(product=product,
                                                                  color=ColorProductModel.objects.get(color=color),
                                                                  size=SizeProductModel.objects.get(size=size),
                                                                  compression_class=compression_class
                                                                  ).exists():
                            ProductVariantModel.objects.create(product=product,
                                                               color=ColorProductModel.objects.get(color=color),
                                                               size=SizeProductModel.objects.get(size=size),
                                                               side=None,
                                                               compression_class=compression_class,
                                                               price=0,
                                                               percent_discount=product.percent_discount,
                                                               quantity=0,
                                                               name=f'{product}-{color}-{size}-{compression_class}')

        variants = ProductVariantModel.objects.filter(product_id=product_id).exclude(
                                                      color__color__in=colors,
                                                      size__size__in=sizes
                                                      )
        variants.delete()

        return Response(data={'message': 'Create'}, status=status.HTTP_201_CREATED)


# Order Section
class OrderFilterView(APIView):
    permission_classes = [IsAdminUser, IsOrderAdmin]

    def get(self, request):
        status_order = self.request.query_params.get('status')

        try:
            order_status = OrderStatusModel.objects.get(status=status_order)

            orders = OrderModel.objects.filter(status=order_status)
        except OrderStatusModel.DoesNotExist:
            return Response({"error": "Invalid status value"}, status=400)

        ser_data = OrderSerializer(instance=orders, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderPaidView(APIView):
    permission_classes = [IsAdminUser, IsOrderAdmin]

    def get(self, request):
        order = OrderModel.objects.filter(paid=True)
        ser_data = OrderSerializer(instance=order, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderUnpaidView(APIView):
    permission_classes = [IsAdminUser, IsOrderAdmin]

    def get(self, request):
        order = OrderModel.objects.filter(paid=False)
        ser_data = OrderSerializer(instance=order, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAdminUser, IsOrderAdmin]

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
    permission_classes = [IsAdminUser, IsOrderAdmin]

    def get(self, request, order_id):
        user = OrderModel.objects.get(id=order_id).user
        ser_data = UserInfoSerializer(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class OrderItemsView(APIView):
    permission_classes = [IsAdminUser, IsOrderAdmin]

    def get(self, request, order_id):
        items = OrderItemModel.objects.filter(order=order_id)
        ser_data = OrderItemSerializer(instance=items, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class CouponView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        coupons = CouponModel.objects.all()
        ser_data = CouponSerializer(instance=coupons, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CouponCreateSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_200_OK)


class CouponItemView(APIView):
    # permission_classes = [IsAdminUser]
    def get(self, request, coupon_id):
        coupon = CouponModel.objects.get(id=coupon_id)
        ser_data = CouponSerializer(instance=coupon)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, coupon_id):
        try:
            coupon = CouponModel.objects.get(id=coupon_id)
        except ProductModel.DoesNotExist:
            return Response(data={'message': 'Coupon does not exist'}, status=status.HTTP_404_NOT_FOUND)

        ser_data = CouponCreateSerializer(instance=coupon, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, coupon_id):
        if coupon_id is None:
            return Response(data={'message': 'Input Coupon ID'})

        try:
            coupon = CouponModel.objects.get(id=coupon_id)
        except:
            return Response(data={'message': 'Coupon is not exist'})

        coupon.delete()

        return Response(data={'message': f'The Coupon ID {coupon_id} was deleted'}, status=status.HTTP_200_OK)


class ContactUsView(APIView):
    def get(self, request):
        contact = ContactSubmitModel.objects.all()
        ser_data = ContactSubmitSerializer(instance=contact, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class ContactUsItemView(APIView):
    def get(self, request, contact_id):
        contact = ContactSubmitModel.objects.get(id=contact_id)
        ser_data = ContactSubmitSerializer(instance=contact)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class SearchOrderView(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['transaction_ref', 'cart_id']
    ordering_fields = '__all__'


class SearchProductView(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product']
    ordering_fields = '__all__'


class SearchBlogView(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = '__all__'


class ManuallyBackupView(APIView):
    def post(self, request):
        try:
            call_command('dbbackup')
            return JsonResponse({'status': 'success', 'message': 'Database backup successful'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class ShippingCountryVIew(APIView):
    def get(self, request):
        countries = ShippingCountryModel.objects.all()
        ser_data = ShippingCountrySerializer(instance=countries, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ShippingCountrySerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)

        return Response(data=ser_data.errors, status=status.HTTP_200_OK)

    def put(self, request, country_id):
        form = request.data
        country = ShippingCountryModel.objects.get(id=country_id)
        ser_data = ShippingCountrySerializer(instance=country, partial=True, data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_200_OK)


class ShippingVIew(APIView):
    def get(self, request, country_id):
        country = ShippingCountryModel.objects.get(id=country_id)
        ser_data = ShippingSerializer(instance=country)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CityShippingSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)

        return Response(data=ser_data.errors, status=status.HTTP_200_OK)

    def put(self, request, city_id):
        form = request.data
        city = ShippingModel.objects.get(id=city_id)
        ser_data = CityShippingSerializer(instance=city, partial=True, data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_200_OK)


class AboutPageView(APIView):
    def get(self, request):
        about = AboutPageModel.objects.all().first()
        ser_data = AboutPageSerializer(instance=about)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, about_id):
        form = request.data
        about = get_object_or_404(AboutPageModel, id=about_id)
        ser_data = AboutPageSerializer(instance=about, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactUsPageView(APIView):
    def get(self, request):
        contact = ContactUsPageModel.objects.all().first()
        ser_data = ContactUsPageSerializer(instance=contact)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, contactus_id):
        form = request.data
        contactus = get_object_or_404(ContactUsPageModel, id=contactus_id)
        ser_data = ContactUsPageSerializer(instance=contactus, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCarePageView(APIView):
    def get(self, request):
        customer = CustomerCarePageModel.objects.all().first()
        ser_data = CustomerCarePageSerializer(instance=customer)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, customerCare_id):
        form = request.data
        customer = get_object_or_404(CustomerCarePageModel, id=customerCare_id)
        ser_data = CustomerCarePageSerializer(instance=customer, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class WholesaleInquiryPageView(APIView):
    def get(self, request):
        wholesale = WholesaleInquiryPageModel.objects.all().first()
        ser_data = WholesaleInquiryPageSerializer(instance=wholesale)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, wholesale_id):
        form = request.data
        wholesale = get_object_or_404(WholesaleInquiryPageModel, id=wholesale_id)
        ser_data = WholesaleInquiryPageSerializer(instance=wholesale, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RefundPolicyPageView(APIView):
    def get(self, request):
        refund = RefundPolicyPageModel.objects.all().first()
        ser_data = RefundPolicyPageSerializer(instance=refund)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, refund_id):
        form = request.data
        refund = get_object_or_404(RefundPolicyPageModel, id=refund_id)
        ser_data = RefundPolicyPageSerializer(instance=refund, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SitemapPageView(APIView):
    def get(self, request):
        sitemap_page = SitemapPageModel.objects.all().first()
        ser_data = SitemapPageSerializer(instance=sitemap_page)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, sitemapPage_id):
        form = request.data
        sitemap_page = get_object_or_404(SitemapPageModel, id=sitemapPage_id)
        ser_data = SitemapPageSerializer(instance=sitemap_page, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CareerPageView(APIView):
    def get(self, request):
        career = CareerPageModel.objects.all().first()
        ser_data = CareerPageSerializer(instance=career)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, career_id):
        form = request.data
        career = get_object_or_404(CareerPageModel, id=career_id)
        ser_data = CareerPageSerializer(instance=career, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopPageView(APIView):
    def get(self, request):
        shop = ShopPageModel.objects.all().first()
        ser_data = ShopPageSerializer(instance=shop)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, shop_id):
        form = request.data
        shop = get_object_or_404(ShopPageModel, id=shop_id)
        ser_data = ShopPageSerializer(instance=shop, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPageView(APIView):
    def get(self, request):
        blog = BlogPageModel.objects.all().first()
        ser_data = BlogPageSerializer(instance=blog)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, blog_id):
        form = request.data
        blog = get_object_or_404(BlogPageModel, id=blog_id)
        ser_data = BlogPageSerializer(instance=blog, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogAuthorView(APIView):
    permission_classes = [IsAdminUser, IsBlogAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def get(self, request):
        author = AuthorBlogModel.objects.all()
        ser_data = BlogAuthorSerializer(instance=author, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BlogAuthorSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogAuthorItemView(APIView):
    permission_classes = [IsAdminUser, IsBlogAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsBlogAdmin, IsSEOAdmin)]
        return super().get_permissions()

    def get(self, request, author_id):
        author = get_object_or_404(AuthorBlogModel, id=author_id)
        ser_data = BlogAuthorSerializer(instance=author)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, author_id):
        form = request.data
        author = AuthorBlogModel.objects.get(id=author_id)
        ser_data = BlogAuthorSerializer(instance=author, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomMadeView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        custom_made = CustomMadeModel.objects.all()
        ser_data = CustomMadeSerializer(instance=custom_made, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CustomMadeSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomMadeItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, custom_id):
        custom_made = get_object_or_404(CustomMadeModel, id=custom_id)
        ser_data = CustomMadeSerializer(instance=custom_made)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, custom_id):
        form = request.data
        author = CustomMadeModel.objects.get(id=custom_id)
        ser_data = CustomMadeSerializer(instance=author, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerTypeView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        custom_made = CustomerTypeModel.objects.all()
        ser_data = CustomerTypeSerializer(instance=custom_made, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CustomerTypeSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerTypeItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, customer_type_id):
        custom_type = get_object_or_404(CustomerTypeModel, id=customer_type_id)
        ser_data = CustomerTypeSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, customer_type_id):
        form = request.data
        custom_type = CustomerTypeModel.objects.get(id=customer_type_id)
        ser_data = CustomerTypeSerializer(instance=custom_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductTypeView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = ProductTypeModel.objects.all()
        ser_data = ProductTypeSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ProductTypeSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductTypeItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, product_type_id):
        custom_type = get_object_or_404(ProductTypeModel, id=product_type_id)
        ser_data = ProductTypeSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, product_type_id):
        form = request.data
        product_type = ProductTypeModel.objects.get(id=product_type_id)
        ser_data = ProductTypeSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BodyAreaView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = BodyAreaModel.objects.all()
        ser_data = BodyAreaSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BodyAreaSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BodyAreaItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, body_area_id):
        custom_type = get_object_or_404(BodyAreaModel, id=body_area_id)
        ser_data = BodyAreaSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, body_area_id):
        form = request.data
        product_type = BodyAreaModel.objects.get(id=body_area_id)
        ser_data = BodyAreaSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassNumberView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = ClassNumberModel.objects.all()
        ser_data = ClassNumberSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = ClassNumberSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassNumberItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, class_num_id):
        custom_type = get_object_or_404(ClassNumberModel, id=class_num_id)
        ser_data = ClassNumberSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, class_num_id):
        form = request.data
        product_type = ClassNumberModel.objects.get(id=class_num_id)
        ser_data = ClassNumberSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TreatmentCategoryView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = TreatmentCategoryModel.objects.all()
        ser_data = TreatmentCategorySerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = TreatmentCategorySerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TreatmentCategoryItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, treatment_category_id):
        custom_type = get_object_or_404(TreatmentCategoryModel, id=treatment_category_id)
        ser_data = TreatmentCategorySerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, treatment_category_id):
        form = request.data
        product_type = TreatmentCategoryModel.objects.get(id=treatment_category_id)
        ser_data = TreatmentCategorySerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class HearAboutUsView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = HearAboutUsModel.objects.all()
        ser_data = HearAboutUsSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = HearAboutUsSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class HearAboutUsItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, hear_about_us_id):
        custom_type = get_object_or_404(HearAboutUsModel, id=hear_about_us_id)
        ser_data = HearAboutUsSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, hear_about_us_id):
        form = request.data
        product_type = HearAboutUsModel.objects.get(id=hear_about_us_id)
        ser_data = HearAboutUsSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CompressionClassView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = CompressionClassModel.objects.all()
        ser_data = CompressionClassSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = CompressionClassSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CompressionClassItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, class_id):
        custom_type = get_object_or_404(CompressionClassModel, id=class_id)
        ser_data = CompressionClassSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, class_id):
        form = request.data
        product_type = CompressionClassModel.objects.get(id=class_id)
        ser_data = CompressionClassSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SideView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = SideModel.objects.all()
        ser_data = SideSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = SideSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SideItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, side_id):
        custom_type = get_object_or_404(SideModel, id=side_id)
        ser_data = SideSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, side_id):
        form = request.data
        product_type = SideModel.objects.get(id=side_id)
        ser_data = SideSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request):
        product_type = ProductBrandModel.objects.all()
        ser_data = BrandSerializer(instance=product_type, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        form = request.data
        ser_data = BrandSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandItemView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def get(self, request, brand_id):
        custom_type = get_object_or_404(ProductBrandModel, id=brand_id)
        ser_data = BrandSerializer(instance=custom_type)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, brand_id):
        form = request.data
        product_type = ProductBrandModel.objects.get(id=brand_id)
        ser_data = BrandSerializer(instance=product_type, data=form, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ManuallyUpdateView(APIView):
    permission_classes = [IsAdminUser, IsProductAdmin]

    def get_permissions(self):
        if self.request.method in ['PUT', 'GET', 'POST']:
            return [OrPermission(IsProductAdmin)]
        return super().get_permissions()

    def post(self, request):
        from product.tasks import zoho_product_update
        # try:
        zoho_product_update()
        return Response({'message': 'Products updated successfully'}, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({'message': f'Error updating products: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



