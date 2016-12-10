from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import logout as acc_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.forms import *
from blog.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# Create your views here.


User = get_user_model()


@csrf_exempt
def register(request):
    userform = UserForm()
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            user = User.objects.create_user(
                username=userform.cleaned_data['username'],
                password=userform.cleaned_data['password'],
            )
            user.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/register.html', {'form': userform, 'form_errors': userform.errors})
    else:
        return render(request, 'registration/register.html', {'form': userform})


@login_required(login_url="/login/")
def logout(request):
    acc_logout(request)
    return HttpResponseRedirect('/')


def home(request):
    bloglist = Blog.objects.all()
    return render(request, 'index.html', {'bloglist': bloglist})


def about(request):
    return render(request, 'about.html')


@login_required(login_url="/login/")
def new(request):
    return render(request, 'new.html')


@csrf_exempt
def contact(request):
    contactform = ContactForm()
    if request.method == 'POST':
        contactform = ContactForm(request.POST, request.FILES)
        if contactform.is_valid():
            contact_form = contactform.save(commit=False)
            contact_form.save()
            file = request.FILES.get('file')
            pic = request.FILES.get('pic')
            subject = 'Thanks for your Interest. We Will Get Back to You Soon'
            message = contact_form.message
            from_email = settings.EMAIL_HOST_USER
            to_list = [contact_form.email]

            mail = EmailMultiAlternatives(subject, message, from_email, to_list)

            if pic:
                mail.attach_file(pic.name, pic.read(), 'image/jpeg')
            if file:
                mail.attach_file(file.name, file.read(), file.content_type)
            mail.send()

            messages.success(request, 'Thank You. We will Get Back')
            return render(request, 'contact.html', {'success': 'success'})
        else:
            print contactform.errors
            return render(request, 'contact.html', {'contactform': contactform})
    else:
        return render(request, 'contact.html', {'contactform': contactform})


def posts(request):
    bloglist = Blog.objects.all()
    return render(request, 'posts.html', {'bloglist': bloglist})


def post(request, pid):
    bloglist = Blog.objects.get(id=pid)
    return render(request, 'post.html', {'bloglist': bloglist})


@staff_member_required
@login_required(login_url="/login/")
@csrf_exempt
def blog(request):
    blogform = BlogForm()
    catlist = Category.objects.all()
    authorlist = Author.objects.all()
    sublist = Subscribe.objects.all()
    if request.method == 'POST':
        blogform = BlogForm(request.POST)
        if blogform.is_valid():
            blog = blogform.save(commit=False)
            blog.save()
            subject = "New Post - Swadesi Blog"
            message = "Hi, You Have a New Post in Swadesi Blog on Present Trending Topic - " + blog.title + "."
            from_email = settings.EMAIL_HOST_USER
            to_list = [s.subscriber_email for s in sublist]

            send_mail(subject, message, from_email, to_list)

            return HttpResponseRedirect('/blog/')
        else:
            return render(request, 'blog.html', {'form': blogform, 'authors': authorlist, 'categories': catlist, 'blog_error': blogform.errors})
    else:
        bloglist = Blog.objects.all()
        return render(request, 'blog.html', {'form': blogform, 'authors': authorlist, 'categories': catlist, 'bloglist': bloglist})


@login_required(login_url="/login/")
def blog_remove(request, bid):
    Blog.objects.filter(id=bid).delete()
    return HttpResponseRedirect('/blog/')


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def author_remove(request, aid):
    Author.objects.filter(id=aid).delete()
    return HttpResponseRedirect('/author/')


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def category_remove(request, cid):
    Category.objects.filter(id=cid).delete()
    return HttpResponseRedirect('/category/')


@login_required(login_url="/login/")
@csrf_exempt
def subscription(request):
    subscriberform = SubscriberForm()
    if request.method == 'POST':
        subscriberform = SubscriberForm(request.POST)
        if subscriberform.is_valid():
            subform = subscriberform.save(commit=False)
            subform.save()
            subject = "Subscription Activated - Swadesi Blog"
            message = "Hi " + subform.subscriber_name + " , Thank You for Subscribing to Swadesi Blog."
            from_email = settings.EMAIL_HOST_USER
            to = [subform.subscriber_email]

            send_mail(subject, message, from_email, to, fail_silently=False)

            data = {"success":"subscribed"}

            return JsonResponse(data)
        else:
            data = {"errors": subscriberform.errors}
            return JsonResponse(data)
    else:
        return render(request, 'index.html', {'sform': subscriberform})
