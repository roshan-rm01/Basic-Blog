from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from .models import Post, Comment
from taggit.models import Tag


def home(request):
    posts = Post.objects.all()[:4]
    return render(request, '../BlogTemplates/index.html', {'posts': posts})


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:post_list')
        else:
            return render(request, '../BlogTemplates/login.html')
    else:
        return render(request, '../BlogTemplates/login.html')


def post_list(request):
    object_list = Post.objects.all()
    if request.method == "POST":
        tag = request.POST['tag']
        tag = tag.strip().lower()
        try:
            tag_obj = get_object_or_404(Tag, name=tag)
            object_list = object_list.filter(tags__in=[tag_obj])
            paginator = Paginator(object_list, 4)
            page = request.GET.get('page', 1)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            return render(request, '../BlogTemplates/all-posts.html', {'posts': posts,
                                                                       'page': page})
        except Http404:
            return redirect("blog:error")
    else:
        paginator = Paginator(object_list, 4)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, '../BlogTemplates/all-posts.html', {'posts': posts,
                                                                   'page': page})


def post_detail(request, slug):
    post = get_object_or_404(Post,
                             slug=slug)
    comment_list = post.comments.filter(active=True)
    if request.method == "POST":
        name = request.POST['name']
        comment = request.POST['comment']
        comment_obj = Comment.objects.create(name=name, body=comment, post=post)
        comment_obj.save()
        paginator = Paginator(comment_list, 4)
        page = request.GET.get('page', 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return render(request, '../BlogTemplates/post.html', {'post': post,
                                                              'comments': comments,
                                                              'page': page})
    else:
        paginator = Paginator(comment_list, 4)
        page = request.GET.get('page', 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return render(request, '../BlogTemplates/post.html', {'post': post,
                                                              'comments': comments,
                                                              'page': page})


def add_post(request):
    if request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        tags = request.POST['tags']
        tags = tags.split(",")
        cleaned_tags = []
        for tag in tags:
            cleaned_tags.append(tag.strip())
        post = Post.objects.create(title=title, slug=slugify(title),
                                   body=body, author=request.user)
        for data in cleaned_tags:
            post.tags.add(data)
        post.save()
        return redirect('blog:post_list')
    else:
        return render(request, '../BlogTemplates/add-post.html')
