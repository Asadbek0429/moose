from math import ceil
from django.shortcuts import render, redirect
from .models import Post, Contact, Comment
import telepot


def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:7]
    d = {
        'posts': posts,
        'home': 'active'
    }
    return render(request, 'index.html', d)


def blog_view(request):
    page = int(request.GET.get('p', 0))
    cat = request.GET.get('cat')

    if cat:
        posts = Post.objects.filter(is_published=True, category_id=cat).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_published=True).order_by('-created_at')

    d = {
        'posts': CPaginator(Post.objects, 6, page),
        'blog': 'active'
    }

    return render(request, 'blog.html', d)


def about_view(request):
    d = {
        'about': 'active',
    }
    return render(request, 'about.html', d)


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

    d = {
        'contact': 'active',
    }
    return render(request, 'contact.html', d)


def detail_view(request, pk):
    if request.method == 'POST':
        d = request.POST
        obj = Comment.objects.create(post_id=int(pk), name=d.get('name'), email=d.get('email'),
                                     website=d.get('website'),
                                     message=d.get('message'))
        obj.save()
        return redirect('/blog/' + str(pk))

    post = Post.objects.filter(id=pk).first()
    comments = Comment.objects.filter(post_id=pk)
    d = {
        'post': post,
        'comments': comments,
        'blog': 'active',
    }
    return render(request, 'blog-single.html', d)


class CPaginator:
    def __init__(self, model, limit, page):
        self.limit = limit
        self.model = model
        self.data = {}
        self.p = page

    def page(self):
        self.data = self.model.raw(
            f"SELECT * FROM blog_post WHERE is_published = true ORDER BY created_at DESC LIMIT {self.limit} OFFSET {self.p * self.limit}")
        return self.data

    def number(self):
        return self.p

    def has_next(self):
        return (self.p + 1) * self.limit < self.model.count()

    def next_page_number(self):
        return str(self.p + 1)

    def has_previous(self):
        return (self.p + 1) * self.limit > self.model.count()

    def previous_page_number(self):
        return str(self.p - 1)

    def page_range(self):
        return range(ceil(self.model.count() / self.limit))
