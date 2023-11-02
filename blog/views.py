from typing import Any
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views import View

from django.conf import settings
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
import os
from uuid import uuid4


class PostListView(ListView):

    model = Post
    template_name = 'blog/post_list.html'


class PostListUserView(ListView):

    model = Post
    template_name = 'blog/my_post.html'

    # 'user' context에 User저장
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.kwargs['blog'])
        return context

    # 이름으로 Post목록을 필터링

    def get_queryset(self):

        return Post.objects.filter(author__username=self.kwargs['blog']).order_by('-created_at')


class PostDeleteView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        
        post = Post.objects.get(pk=pk)
        
        if post.author != request.user and not request.user.is_superuser:
            return redirect('blog:post_detail', pk)
        post.delete()
        
        return redirect('blog:post_list')
    

class PostPopularView(ListView):

    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.all().order_by('-views')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = {'popular': '인기글'}
        return context


class PostDetailView(DetailView):

    template_name = 'blog/post_detail.html'
    queryset = Post.objects.all()

    def get_object(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.views += 1
        post.save()
        return post


class PostCreateView(LoginRequiredMixin, CreateView):

    template_name = 'blog/post_create.html'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.views -= 1

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):

    template_name = 'blog/post_create.html'
    model = Post
    form_class = PostForm

    def get_object(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # 글을 수정할 시 작성한 회원이거나 관리자만 글을 수정할 수 있음.
        if post.author == self.request.user or self.request.user.is_superuser:
            return post
        else:
            raise PermissionDenied('글을 수정할 수 있는 권한이 없습니다!')

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


def fileUpload(request):
    if request.method == 'POST' or request.method == 'GET':
        # 업로드된 파일을 가져옵니다.
        uploaded_file = request.FILES.get('images')
        uuid = str(uuid4())
        if uploaded_file:
            # 파일 확장자를 추출합니다 (xxx.png)
            file_extension = uploaded_file.name.split('.')[-1]

            # 파일을 저장합니다. (---uuid----.png)
            file_name = os.path.join(
                'media/blog/images/', f'{uuid}.{file_extension}')
            with open(file_name, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            print(file_name)
            # 파일의 URL을 생성합니다. (---uuid----.png)
            file_url = settings.MEDIA_URL + os.path.join(
                'blog/images/', f'{uuid}.{file_extension}')
            print(file_url)
            return JsonResponse({
                'success': True,
                'url': file_url,
            })
        else:
            return JsonResponse({
                'success': False,
                'error': '이미지를 찾을 수 없습니다.',
            })
    else:
        return JsonResponse({
            'success': False,
            'error': '비정상적인 접근입니다.',
        })
