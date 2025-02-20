from django.urls import path
from .views import register,login_view,log_out,update_profile,profile,create_blog,my_blogs,update_blog,delete_blog,sending_mail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('create_blog/', create_blog, name='create_blog'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('update_blog/<int:id>', update_blog, name='update_blog'),
    path('delete_blog/<int:id>', delete_blog, name='delete_blog'),
    path('sending_mail/', sending_mail, name='sending_mail'), 
]

