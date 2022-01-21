from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    # path('base.html', views.Base.as_view(), name='base'), #テスト2022/1/19
]