from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # Blog
    path('list/', views.BlogListView.as_view(), name='blog_list'),
    path('land/', views.BlogListView.as_view(), name='blog_land'),
    path('related/', views.RelatedPostView.as_view(), name='blog_related'),
    path('item/<str:slug>/', views.BlogView.as_view(), name='blog'),
    path('comment/<int:blog_id>/', views.CommentBlogView.as_view(), name='comment'),
    path('comment/reply/<int:blog_id>/<int:comment_id>/', views.ReplyCommentView.as_view(), name='comment_reply'),
    path('comment/create/<int:blog_id>/', views.CommentBlogView.as_view(), name='comment_create'),
    path('search/', views.SearchBlogView.as_view({'get': 'list'}), name='search_blog'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),

]
