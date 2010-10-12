from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from keptar.utils import get_abspath
import os.path

class PBlogEntry(models.Model):
    """PhotoBlog "bejegyzes", azaz egy olyan kep, amit megjeloltunk, hogy
    megjelenjen a blog reszben
    """

    path = models.CharField(max_length=1000, unique=True)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    mark_date = models.DateTimeField('date marked', auto_now_add=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'PBlog bejegyzes'
        verbose_name_plural = 'PBlog bejegyzesek'

    def is_valid(self):
        """ellenorzi, hogy a 'path' utvonalon levo file letezik-e"""
        
        abspath = get_abspath(self.path)

        return os.path.isfile(abspath)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.path)
