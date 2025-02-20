from .models import FooterImages,Blog
from report.models import Contact


def common_data(request):

    latest_blogs = Blog.objects.filter(status = Blog.StatusEnum.PUBLISHED).order_by('-update_time')[:5]
    footer = FooterImages.objects.all()
    contact = Contact.objects.last()


    context = {
        'latest_blogs':latest_blogs,
        'footer':footer,
        'contact':contact
    }

    return context