from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import BlogModel, BlogCategoryModel, CommentBlogModel
from .serializers import (BlogSerializer, BlogAllSerializer, RelatedBlogSerializer, MetaCategorySerializer,
                          CommentBlogSerializer, CommentCreateSerializer)
import math
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class BlogListView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)

        per_page = 16
        blog_count = len(BlogModel.objects.all())
        number_of_pages = math.ceil(blog_count / per_page)
        if limit is not None:
            blog = BlogModel.objects.all()[:int(limit)]
            ser_data = BlogAllSerializer(instance=blog, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)

        if page is not None:
            page = int(page)
            blog = BlogModel.objects.all()[per_page*(page-1):per_page*page]
        else:
            blog = BlogModel.objects.all()

        ser_data = BlogAllSerializer(instance=blog, many=True)
        return Response({'data': ser_data.data, 'number_of_pages': number_of_pages}, status=status.HTTP_200_OK)


class BlogView(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(BlogModel, slug=slug)
        ser_data = BlogSerializer(instance=blog)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class RelatedPostView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        category = self.request.query_params.get('category', None)
        page = self.request.query_params.get('page', None)

        per_page = 10
        blog_count = len(BlogModel.objects.all())
        number_of_pages = math.ceil(blog_count / per_page)

        category = get_object_or_404(BlogCategoryModel, category=category)
        if limit is not None:
            blog = BlogModel.objects.filter(category=category)[:int(limit)]
        else:
            blog = BlogModel.objects.filter(category=category)

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
        blog = get_object_or_404(BlogModel, id=blog_id)
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
        blog = get_object_or_404(BlogModel, id=blog_id)
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
