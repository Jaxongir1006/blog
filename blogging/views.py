from django.shortcuts import render,redirect
from .models import Blog,Comment,Category,FooterImages
from .forms import CommentForm
from user.models import Profile
from django.http.response import JsonResponse
from history.models import Saved
from report.models import Contact
from django.db.models import Count
from django.core.paginator import Paginator
from history.models import History


# FBV -> function based view
# CBV -> class based view

def home(request):
    blogs = Blog.objects.comment_count().order_by('-update_time')
    categories = Category.objects.category_blog_count()[:4]
    header_blogs = []
    main_blog = Blog.objects.annotate(comment_count = Count('comment')).last()

    temp = []
    for blog in blogs:
        temp.append(blog)
        if len(temp) == 4:
            header_blogs.append(temp)
            temp = []

    context = {
        'blogs':blogs,
        'categories': categories,
        'header_blogs':header_blogs,
        'main_blog':main_blog,
    }

    return render(request, 'new/index.html', context)

def blogs(request, category = None):
    blogs = Blog.objects.annotate(comment_count = Count('comment'))
    categories = Category.objects.annotate(blog_count = Count('blog')).all()


    if category:
        category = Category.objects.get(id = category)
        blogs = blogs.filter(category = category)

    title = request.GET.get('title', None)

    if title:
        blogs = blogs.filter(title__icontains = title)
    

    paginator = Paginator(blogs, per_page=3)

    page = request.GET.get('page', 1)

    blogs = paginator.get_page(page)


    context = {
        'blogs':blogs,
        'category':category,
        'categories':categories,
    }


    return render(request, 'new/blogs.html', context)

def about(request):
    return render(request, 'new/about.html')

def contact_us(request):
    return render(request, 'new/contact.html')



def blog_details(request, id):
    blog = Blog.objects.annotate(comment_count = Count('comment')).get(id = id)

    check2 = False
    if blog in Saved.objects.all():
        check2 = True

    seen = request.session.get(f'blog_{blog.id}', None)
    if not seen:
        blog.add_view
        request.session[f'blog_{blog.id}'] = blog.id

    check = False
    if hasattr(request.user,'profile'):
        author = blog.author
        check = author.subscribers.filter(id=request.user.profile.id).exists()
        History.objects.get_or_create(user = request.user.profile, blog = blog)

    other_blogs = Blog.objects.filter(author = blog.author).exclude(id = blog.id)

    previous = None
    next = None

    if other_blogs.exists():
        if len(other_blogs) >= 2:
            previous = other_blogs.first()
            next = other_blogs.last()
        else:
            next = other_blogs[0]

    comments = Comment.objects.filter(blog = blog, reply__isnull = True)
    form = CommentForm()
    context = {
        'blog':blog,
        'comments':comments,
        'form':form,
        'check':check,
        'check2':check2,
        'next':next,
        'previous':previous
    }
    return render(request, 'new/blog_details.html', context)


def create_comment(request, id):
    if request.method == 'POST':
        print(request.POST)
        blog = Blog.objects.get(id = id)

        form = CommentForm(request.POST)
        if form.is_valid():

            form.instance.blog = blog
            form.instance.user = request.user.profile

            form.save()
        else:
            print(form.errors)

    return redirect(request.META.get("HTTP_REFERER"))


def like_view(request, id):
    if hasattr(request.user,'profile'):
        blog = Blog.objects.get(id = id)
        blog.add_like(request.user.profile)
    return JsonResponse({'like':blog.likes.count()})


def dislike_view(request, id):
    if hasattr(request.user,'profile'):
        blog = Blog.objects.get(id = id)
        blog.add_dislike(request.user.profile)
    return JsonResponse({'like':blog.likes.count(), 'dislike':blog.dislike.count()})


def subscribe(request,author_id):
    if hasattr(request.user,'profile'):
        user = Profile.objects.get(id = author_id)
        check = user.subscribe(request.user.profile)
    return JsonResponse({'check':check})

def save_blog(request, id):

    blog = Blog.objects.get(id = id)
    check2 = False
    if hasattr(request.user,'profile'):
        blogs = Saved.objects.filter(user = request.user.profile,blog = blog)
        if blogs.exists():
            blogs.delete()
        else:
            Saved.objects.create(user = request.user.profile,blog = blog)
            check2 = True

    return JsonResponse({"check2":check2})

