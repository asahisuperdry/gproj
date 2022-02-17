# from multiprocessing import context
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception  = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user

class Index(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('app:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Postを登録しました')
        return resolve_url('app:index')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        detail_data = Post.objects.get(id = self.kwargs['pk'])
        category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        return params


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'Postを更新しました')
        return resolve_url('app:post_detail', pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin, DeleteView):
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


@login_required
def Like_add(request, post_id):
    post = Post.objects.get(id = post_id)
    is_liked = Like.objects.filter(user = request.user).filter(post = post_id).count()
    if is_liked > 0:
        messages.info(request, 'すでにお気に入りに追加済みです')
        return redirect('app:post_detail', post_id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()

    messages.success(request, 'お気に入りに追加しました！')
    return redirect('app:post_detail', post.id)


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')

        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }

        return params

