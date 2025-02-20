from .views import home,blog_details,create_comment,like_view,dislike_view,subscribe,save_blog,blogs,contact_us,about
from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url = "home"), name='main'), 
    path('home/', home, name='home'), 
    path('blog_details/<int:id>/', blog_details, name='blog_details'), 
    path('create_comment/<int:id>/', create_comment, name='create_comment'), 
    path('like_view/<int:id>/', like_view, name='like_view'), 
    path('dislike_view/<int:id>/', dislike_view, name='dislike_view'), 
    path('subscribe/<int:author_id>/', subscribe, name='subscribe'),
    path('save_blog/<int:id>/', save_blog, name='save_blog'), 
    path('blogs/<int:category>/', blogs, name='blogs'), 
    path('blogs/', blogs, name='blogs_filter'), 
    path('contact_us/', contact_us, name='contact_us'), 
    path('about/', about, name='about'), 
]