from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('list/', views.BLogListView.as_view(), name='blog_list'),
    path('land/', views.BLogListView.as_view(), name='blog_land'),
    path('related/', views.RelatedPostView.as_view(), name='blog_related'),
    path('<str:slug>/', views.BlogView.as_view(), name='blog'),
]