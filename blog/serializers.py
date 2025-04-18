from rest_framework import serializers
from .models import BlogModel, AddBlogTagModel, BlogCategoryModel, BlogImageModel, CommentBlogModel, AuthorBlogModel


class BlogSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
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

    def get_categories(self, obj):
        categories = obj.cat_blog.all()
        categories = [category.category.category for category in categories]
        return categories


class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorBlogModel
        fields = '__all__'


class BlogAllSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer()
    created = serializers.DateTimeField(format="%d. %B %Y", read_only=True)
    updated = serializers.DateTimeField(format="%d. %B %Y", read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created', 'updated',
                  'read_duration', 'author', 'category', 'is_active']

    def get_category(self, obj):
        categories = obj.cat_blog.all()
        categories = [category.category.category for category in categories]
        return categories


class RelatedBlogSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d %b %Y')

    class Meta:
        model = BlogModel
        fields = ['id', 'cover_image', 'title', 'short_description', 'slug', 'created', 'is_active']


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
    author = BlogAuthorSerializer()
    updated = serializers.DateTimeField(format="%d. %B %Y", read_only=True)

    class Meta:
        model = BlogModel
        fields = ['title', 'short_description', 'author', 'updated', 'slug', 'is_active']


class GetBlogSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer()
    tag = serializers.SerializerMethodField()
    all_categories = serializers.SerializerMethodField()
    recent_blog = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    canonical = serializers.CharField(max_length=256, required=False, allow_blank=True)
    meta_title = serializers.CharField(max_length=60, required=False, allow_null=True)
    meta_description = serializers.CharField(max_length=160, required=False, allow_null=True)
    schema_markup = serializers.CharField(required=False, allow_null=True)
    created = serializers.DateTimeField(format="%d. %B %Y", read_only=True)
    updated = serializers.DateTimeField(format="%d. %B %Y", read_only=True)

    class Meta:
        model = BlogModel
        fields = ['id', 'tag', 'category', 'canonical', 'meta_title', 'meta_description', 'schema_markup',
                  'title', 'short_description', 'all_categories', 'recent_blog', 'author', 'created',
                  'updated', 'comments', 'body', 'comments_count', 'read_duration', 'slug', 'is_active', 'cover_image',
                  'cover_image_alt']

    def get_category(self, obj):
        categories = obj.cat_blog.all()
        categories = [category.category.category for category in categories]
        return categories

    def get_comments(self, obj):
        comments = obj.blogcomment.filter(is_active=True)
        return CommentBlogSerializer(comments, many=True).data

    def get_comments_count(self, obj):
        comments_count = len(obj.blogcomment.filter(is_reply=False))

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
