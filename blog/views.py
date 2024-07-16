from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import BlogModel, BlogCategoryModel
from .serializers import BlogSerializer, BlogAllSerializer, RelatedBlogSerializer, MetaCategorySerializer
import math
from rest_framework import status


class BLogListView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)

        per_page = 16
        blog_count = len(BlogModel.objects.all())
        number_of_pages = math.ceil(blog_count / per_page)
        if limit is not None:
            blog = BlogModel.objects.all()[:int(limit)]
            ser_data = BlogAllSerializer(instance=blog, many=True)
            return Response(data=ser_data.data)

        if page is not None:
            page = int(page)
            blog = BlogModel.objects.all()[per_page*(page-1):per_page*page]
        else:
            blog = BlogModel.objects.all()

        ser_data = BlogAllSerializer(instance=blog, many=True)
        return Response({'data': ser_data.data, 'number_of_pages': number_of_pages})


class BlogView(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(BlogModel, slug=slug)
        ser_data = BlogSerializer(instance=blog)
        return Response(data=ser_data.data)


class RelatedPostView(APIView):
    def get(self, request):
        limit = self.request.query_params.get('limit', None)
        category = self.request.query_params.get('category', None)
        category = get_object_or_404(BlogCategoryModel, category=category)
        if limit is not None:
            blog = BlogModel.objects.filter(category=category)[:int(limit)]
        else:
            blog = BlogModel.objects.filter(category=category)
        ser_data = RelatedBlogSerializer(instance=blog, many=True)

        ser_meta = MetaCategorySerializer(instance=category)
        return Response(data={'data': ser_data.data, 'meta': ser_meta.data})



