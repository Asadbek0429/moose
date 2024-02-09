from django.shortcuts import render, redirect
from .models import Post, Contact, Comment
import telepot
from django.core.paginator import Paginator


def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:7]
    d = {
        'posts': posts
    }
    return render(request, 'index.html', d)


def blog_view(request):
    page = request.GET.get('p', 1)
    cat = request.GET.get('cat')
    if cat:
        posts = Post.objects.filter(is_published=True, category_id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')

    paginator = Paginator(posts, 6)
    d = {
        'posts': paginator.page(page),
    }

    return render(request, 'blog.html', d)


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        d = request.POST
        obj = Contact.objects.create(name=d.get('name'), email=d.get('email'), subject=d.get('subject'),
                                     message=d.get('message'))
        obj.save()

        telegramBot = telepot.Bot('6601466546:AAFmwhsxCRsEglPR2jBBCZIclWesYZe7HS8')
        text = f'Name: {d.get("name")} \nEmail: {d.get("email")} \nMessage: {d.get("message")}'
        telegramBot.sendMessage(-1002084571362, text, parse_mode="Markdown")

        return redirect('/contact')
    return render(request, 'contact.html')


def detail_view(request, pk):
    if request.method == 'POST':
        d = request.POST
        obj = Comment.objects.create(post_id=int(pk), name=d.get('name'), email=d.get('email'),
                                     website=d.get('website'),
                                     message=d.get('message'))
        obj.save()
        return redirect('/blog/' + pk)

    post = Post.objects.filter(id=pk).first()
    comments = Comment.objects.filter(post_id=pk)
    d = {
        'post': post,
        'comments': comments
    }
    return render(request, 'blog-single.html', d)
