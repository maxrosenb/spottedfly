from django.shortcuts import render
from blog.models import Post # < here


def index(request, slug=None): # < here
    posts = Post.objects.all()
    return render(request,
                  'blog/index.html',
                  {
                      'posts': posts,
                      'section': 'blog_index'
                  })


def detail(request, slug=None): # < here
    post = Post.objects.get(slug=slug)
    return render(request,
                  'blog/detail.html',
                  {
                      'post': post,
                      'section': 'blog_detail'
                  })


def home(request): # < here
    return render(request,
                  'home.html',
                  {'section': 'home'})