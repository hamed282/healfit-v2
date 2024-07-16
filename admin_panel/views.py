from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import User, RoleModel
from .serializers import UserSerializer, UserValueSerializer, RoleSerializer, LoginUserSerializer
from accounts.serializers import UserRegisterSerializer
from rest_framework import status
from math import ceil
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserLoginSerializer
from blog.serializers import BlogAllSerializer, BlogSerializer, BlogTagSerializer
from blog.models import BlogModel, BlogTagModel


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
    def get(self, request):
        page = self.request.query_params.get('page', None)

        per_page = 20
        product_count = len(User.objects.all())
        number_of_pages = ceil(product_count / per_page)

        if page is not None:
            page = int(page)
            product = User.objects.all()[per_page*(page-1):per_page*page]
        else:
            product = User.objects.all()

        ser_data = UserSerializer(instance=product, many=True)
        return Response({'data': ser_data.data, 'number_of_pages': number_of_pages})


class RoleView(APIView):
    def get(self, request):
        role = RoleModel.objects.all()
        ser_data = RoleSerializer(instance=role, many=True)
        return Response(data=ser_data.data)


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
    def get(self, request):
        blogs = BlogModel.objects.all()
        ser_data = BlogAllSerializer(instance=blogs, many=True)
        return Response(data=ser_data.data)


class BlogView(APIView):
    def get(self, request, blog_id):
        blog = get_object_or_404(BlogModel, id=blog_id)
        ser_data = BlogSerializer(instance=blog)
        return Response(data=ser_data.data)

    def post(self, request):
        form = request.data

        ser_data = BlogSerializer(data=form)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id):
        if blog_id is None:
            return Response(data={'message': 'Input Blog ID'})
        try:
            blog = BlogModel.objects.get(id=blog_id)
        except:
            return Response(data={'message': 'Blog is not exist'})

        ser_data = BlogSerializer(instance=blog, data=request.data, partial=True)

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


class BLogTagListView(APIView):
    def get(self, request):
        blog_tag = BlogTagModel.objects.all()
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
    def get(self, request, tag_id):
        tag = get_object_or_404(BlogTagModel, id=tag_id)
        ser_data = BlogTagSerializer(instance=tag)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

