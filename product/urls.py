from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('gender_home/', views.ProductGenderView.as_view(), name='gender_home'),

]
