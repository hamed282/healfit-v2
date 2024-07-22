from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('image_slider/', views.ImageSliderView.as_view(), name='image_slider'),
    path('video/', views.VideoHomeView.as_view(), name='video'),
    path('comment/', views.CommentHomeView.as_view(), name='comment'),

]
