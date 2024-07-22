from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('image_slider/', views.ImageSliderView.as_view(), name='image_slider'),

]
