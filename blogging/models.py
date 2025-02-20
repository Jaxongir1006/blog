from django.db import models
from .managers import BlogManager,CategoryManager
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

class Category(TranslatableModel):

    translations = TranslatedFields(
        name = models.CharField(verbose_name=_('name'), max_length=200,blank=True,null=True)
    )

    image = models.ImageField(verbose_name=_('image'),upload_to="Category_images/",blank=True, null=True)
    
    def __str__(self):
        return self.safe_translation_getter('name') or "None"

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    objects = CategoryManager()



    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''


class Blog(TranslatableModel):

    class StatusEnum(models.TextChoices):
        PUBLISHED = 'published'
        DRAFT = 'draft'
        BLOCKED = 'blocked'

    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        description = models.TextField()
    )

    author = models.ForeignKey('user.Profile', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/')
    likes  = models.ManyToManyField('user.Profile', related_name='likes', blank=True)
    dislike  = models.ManyToManyField('user.Profile', related_name='dislikes', blank=True)
    view = models.IntegerField(default=1)
    status  = models.CharField(max_length=10, choices=StatusEnum.choices, default=StatusEnum.DRAFT)
    created_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    class Meta:
        ordering = ['-update_time']
        verbose_name = _('Yangi blog')
        verbose_name_plural = _('Yangi bloglar')


    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
    def add_like(self, profile):
        if not profile in self.likes.all():
            self.likes.add(profile)
        else:
            self.likes.remove(profile)
        self.dislike.remove(profile)

    def add_dislike(self, profile):
        if not profile in self.dislike.all():
            self.dislike.add(profile)
        else:
            self.dislike.remove(profile)
        self.likes.remove(profile)
    
    @property
    def add_view(self):
        self.view += 1
        self.save()
    


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    text = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True, related_name='replies')
    like = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class FooterImages(models.Model):
    image = models.ImageField(upload_to='footer_images/')

    class Meta:
        verbose_name_plural = _('FooterImages')

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
    class Meta:
        verbose_name = _('FooterImage')
        verbose_name_plural = _('FooterImages')