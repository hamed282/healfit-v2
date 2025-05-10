from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import BlogModel, BlogCategoryModel, CommentBlogModel
from .serializers import (GetBlogSerializer, BlogAllSerializer, RelatedBlogSerializer, MetaCategorySerializer,
                          CommentBlogSerializer, CommentCreateSerializer, BlogCategorySerializer)
import math
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class BlogListView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)
        category = self.request.query_params.get('category', None)

        blogs = BlogModel.objects.filter(is_active=True).order_by('-created')
        
        if category:
            # Get blogs that have this category through AddCategoryModel
            blogs = blogs.filter(cat_blog__category__category=category)

        blog_count = len(blogs)
        per_page = 16
        number_of_pages = math.ceil(blog_count / per_page)

        if limit is not None:
            blogs = blogs[:int(limit)]
            ser_data = BlogAllSerializer(instance=blogs, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)

        if page is not None:
            page = int(page)
            blogs = blogs[per_page*(page-1):per_page*page]

        ser_data = BlogAllSerializer(instance=blogs, many=True)
        return Response({'data': ser_data.data, 'number_of_pages': number_of_pages}, status=status.HTTP_200_OK)


class BlogView(APIView):
    def get(self, request, slug):
        try:
            blog = get_object_or_404(BlogModel, slug=slug, is_active=True)
            ser_data = GetBlogSerializer(instance=blog)
            print(ser_data)

            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


class RelatedPostView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        category = self.request.query_params.get('category', None)
        page = self.request.query_params.get('page', None)

        per_page = 10
        blog_count = len(BlogModel.objects.filter(is_active=True))
        number_of_pages = math.ceil(blog_count / per_page)

        category = get_object_or_404(BlogCategoryModel, category=category)
        if limit is not None:
            blog = BlogModel.objects.filter(is_active=True, category=category)[:int(limit)]
        else:
            blog = BlogModel.objects.filter(is_active=True, category=category)

        if page is not None:
            page = int(page)
            blog = blog[per_page*(page-1):per_page*page]
        else:
            blog = blog

        ser_data = RelatedBlogSerializer(instance=blog, many=True)

        ser_meta = MetaCategorySerializer(instance=category)
        return Response(data={'data': ser_data.data, 'meta': ser_meta.data, 'number_of_pages': number_of_pages},
                        status=status.HTTP_200_OK)


class CommentBlogView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id):
        comments = CommentBlogModel.objects.filter(blog=blog_id, is_active=True)
        ser_data = CommentBlogSerializer(instance=comments, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, blog_id):
        blog = get_object_or_404(BlogModel, id=blog_id, is_active=True)
        form = request.data
        ser_data = CommentCreateSerializer(data=form)
        if ser_data.is_valid():
            CommentBlogModel.objects.create(user=request.user,
                                            blog=blog,
                                            body=form['body'])
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id, comment_id):
        blog = get_object_or_404(BlogModel, id=blog_id, is_active=True)
        comment = get_object_or_404(CommentBlogModel, id=comment_id)
        form = request.data
        ser_data = CommentCreateSerializer(data=form)
        if ser_data.is_valid():
            CommentBlogModel.objects.create(user=request.user,
                                            blog=blog,
                                            reply=comment,
                                            is_reply=True,
                                            body=form['body'])
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchBlogView(viewsets.ModelViewSet):
    queryset = BlogModel.objects.filter(is_active=True)
    serializer_class = GetBlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['body', 'short_description', 'title']
    ordering_fields = '__all__'

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        if not search_query:
            return Response({"detail": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)


class CategoryListView(APIView):
    def get(self, request):
        categories = BlogCategoryModel.objects.all()
        ser_data = BlogCategorySerializer(instance=categories, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
