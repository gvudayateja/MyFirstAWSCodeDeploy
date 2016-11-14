from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@login_required(login_url="/")
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    bloglist = Blog.objects.all()
    return render(request, 'index.html', {'bloglist': bloglist})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def post(request, pid):
    bloglist = Blog.objects.get(id=pid)
    return render(request, 'post.html', {'bloglist': bloglist})


@csrf_exempt
def blog(request):
    blogform = BlogForm()
    catlist = Category.objects.all()
    authorlist = Author.objects.all()
    if request.method == 'POST':
        blogform = BlogForm(request.POST)
        if blogform.is_valid():
            blogform.save()
            return HttpResponseRedirect('/blog/')
        else:
            return render(request, 'blog.html', {'form': blogform, 'authorform': authorlist, 'catform': catlist, 'blog_error': blogform_errors})
    else:
        bloglist = Blog.objects.all()
        return render(request, 'blog.html', {'form': blogform, 'authorform': authorlist, 'catform': catlist, 'bloglist': bloglist})


def blog_remove(request, bid):
    Blog.objects.filter(id=bid).delete()
    return HttpResponseRedirect('/blog/')


@csrf_exempt
def author(request):
    authform = AuthorForm()
    if request.method == 'POST':
        authform = AuthorForm(request.POST)
        if authform.is_valid():
            authform.save()
            return HttpResponseRedirect('/author/')
        else:
            return render(request, 'author.html', {'form': authform, 'auth_error': authform.errors})
    else:
        authlist = Author.objects.all()
        return render(request, 'author.html', {'form': authform, 'authlist': authlist})


def author_remove(request, aid):
    Author.objects.filter(id=aid).delete()
    return HttpResponseRedirect('/author/')


@csrf_exempt
def category(request):
    catform = CategoryForm
    if request.method == 'POST':
        catform = CategoryForm(request.POST)
        if catform.is_valid():
            catform.save()
            return HttpResponseRedirect('/category/')
        else:
            return render(request, 'category.html', {'form': catform, 'cat_error': catform.errors})
    else:
        catlist = Category.objects.all()
        return render(request, 'category.html', {'form': catform, 'catlist': catlist})


def category_remove(request, cid):
    Category.objects.filter(id=cid).delete()
    return HttpResponseRedirect('/category/')


# @csrf_exempt
# def bloglist(request):
#   bloglist = Blog.objects.all()
#   return render(request, 'blog.html', {'bloglist': bloglist})


# def execution(request):
#     Blog.objects.all()
#     Blog.objects.create(title="First", author=Author.objects.filter(exp='PROFESSIONAL',
#         firstname="MicroPyr", lastname="Info"
#         ), category=Category.objects.create(
#         name="Beverages", desc="This is the Place where we get posts on Beverages"
#         ),
#         description="My First Post has been Posted")
#     Author.objects.filter(firstname="MicroPyr").update(firstname="Micropyramid")
#     Category.objects.get(id=8).update(name="Foodies Blog")
#     Blog.objects.filter(title="First Post").update(title="My First Post")
#     Blog.objects.filter(id=8).delete()
#     print "Post has been Created"
