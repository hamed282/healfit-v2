from rest_framework import serializers
from .models import BlogModel, AddBlogTagModel, BlogCategoryModel, BlogImageModel, CommentBlogModel


class BlogSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='category', queryset=BlogCategoryModel.objects.all(),)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_null=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_null=True)
    schema_markup = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = BlogModel
        fields = '__all__'

    def get_tag(self, obj):
        try:
            tag = AddBlogTagModel.objects.get(blog=obj)
            tag = tag.tag.id
        except:
            tag = None

        return tag


class BlogAllSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class RelatedBlogSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created']


class MetaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'


class ImageBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImageModel
        fields = '__all__'


class CommentBlogSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d %b %Y - %H:%m')
    user = serializers.SlugRelatedField(read_only=True, slug_field='first_name')

    class Meta:
        model = CommentBlogModel
        fields = ['id', 'is_reply', 'body', 'created', 'user', 'reply']


class CommentCreateSerializer(serializers.Serializer):
    body = serializers.CharField()


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryModel
        fields = ['id', 'category', 'slug']


class RecentBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = ['title', 'short_description', 'author', 'updated', 'slug']


class GetBlogSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    all_categories = serializers.SerializerMethodField()
    recent_blog = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='category', queryset=BlogCategoryModel.objects.all(),)
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_null=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_null=True)
    schema_markup = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = BlogModel
        fields = ['id', 'tag', 'category', 'canonical', 'meta_title', 'meta_description', 'schema_markup', 'banner',
                  'banner_alt', 'title', 'short_description', 'all_categories', 'recent_blog', 'author', 'created',
                  'updated', 'comments', 'body', 'comments_count']

    def get_comments(self, obj):
        comments = obj.blogcomment.all()
        return CommentBlogSerializer(comments, many=True).data

    def get_comments_count(self, obj):
        comments_count = len(obj.blogcomment.filter(reply=False))

        return comments_count

    def get_all_categories(self, obj):
        categories = BlogCategoryModel.objects.all()
        return BlogCategorySerializer(instance=categories, many=True).data

    def get_recent_blog(self, obj):
        blogs = BlogModel.objects.all()[:3]
        return RecentBlogSerializer(instance=blogs, many=True).data

    def get_tag(self, obj):
        try:
            tag = AddBlogTagModel.objects.get(blog=obj)
            tag = tag.tag.id
        except:
            tag = None

        return tag
