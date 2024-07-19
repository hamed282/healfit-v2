from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # Blog
    path('list/', views.BlogListView.as_view(), name='blog_list'),
    path('land/', views.BlogListView.as_view(), name='blog_land'),
    path('related/', views.RelatedPostView.as_view(), name='blog_related'),
    path('item/<str:slug>/', views.BlogView.as_view(), name='blog'),
]
