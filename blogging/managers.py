from django.db.models import Manager,Count
from parler.models import TranslatableManager

class BlogManager(Manager):
    
    def published_blogs(self):
        return self.get_queryset().filter(status = 'published')

    def latest_blogs(self):
        return self.published_blogs().last()

    def comment_count(self):
        return self.published_blogs().annotate(comment_count = Count('comment'))


class CategoryManager(TranslatableManager):
    def category_blog_count(self):
        return self.get_queryset().annotate(blog_count = Count('blog'))