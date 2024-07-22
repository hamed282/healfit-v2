from django.urls import path
from . import views


app_name = 'admin_panel'
urlpatterns = [
    # Accounts
    path('user/', views.UserView.as_view(), name='users'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user_id'),
    path('user/all/', views.UserValueView.as_view(), name='user_all'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('login/', views.LoginUserView.as_view(), name='login'),

    # General
    path('language/active/', views.LanguageView.as_view(), name='language'),

    # Blog
    path('blog/list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/', views.BlogView.as_view(), name='blog_item_get'),
    path('blog/item/', views.BlogView.as_view(), name='blog_item'),

    # Blog Tag
    path('blog/tag/', views.BLogTagListView.as_view(), name='tag_list'),
    path('blog/tag/<int:tag_id>/', views.BLogTagListView.as_view(), name='tag_create'),
    path('blog/tag/item/<int:tag_id>/', views.BLogTagItemView.as_view(), name='tag_item'),

    # Add Blog Tag
    path('blog/addtag/', views.AddBLogTagListView.as_view(), name='addtag_post'),
    path('blog/addtag/<int:blog_id>/', views.AddBLogTagListView.as_view(), name='addtag'),

    # Blog Category
    path('blog/category/', views.BlogCategoryView.as_view(), name='category'),
    path('blog/category/<int:category_id>/', views.BlogCategoryView.as_view(), name='category_put'),

    # Home
    path('home/comment/', views.CommentHomeView.as_view(), name='comment'),
    path('home/comment/item/', views.CommentItemView.as_view(), name='comment_item'),
    path('home/comment/item/<int:comment_id>/', views.CommentItemView.as_view(), name='comment_id'),

    path('home/banner/', views.BannerHomeView.as_view(), name='banner'),
    path('home/banner/item/', views.BannerItemView.as_view(), name='banner_item'),
    path('home/banner/item/<int:banner_id>/', views.BannerItemView.as_view(), name='banner_id'),

]
