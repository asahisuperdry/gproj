# from multiprocessing import context
from django.shortcuts import render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login


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
    success_url = reverse_lazy('app :index')


class PostDetail(DetailView):
    model = Post


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'Postを更新しました')
        return resolve_url('app:post_detail', pk=self.kwargs['pk'])

class PostDelete(DeleteView):
    model = Post

    def get_success_url(self):
        messages.info(self.request, 'Postを削除しました')
        return resolve_url('app:index')


class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'


class Logout(LogoutView):
    template_name = 'app/logout.html'


class SignUp(CreateView):
    form_class = SignupForm
    template_name = 'app/signup.html'
    # success_url = reverse_lazy('app:post_create')
    success_url = reverse_lazy('app:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザーを登録しました')
        return HttpResponseRedirect(self.get_success_url())
        # messages.success(self.request, '登録しました')
        # return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力内容ををご確認ください')
        return super().form_invalid(form)


