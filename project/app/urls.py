from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('base.html', views.Index.as_view(), name='base'),
]