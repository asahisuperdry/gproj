from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm


class Index(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('app:index')



# #テスト2022/1/19
# class Base(TemplateView):
#     template_name = 'app/base.html'
