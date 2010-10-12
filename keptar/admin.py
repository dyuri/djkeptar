from keptar.models import PBlogEntry
from django.contrib import admin

class PBlogEntryAdmin(admin.ModelAdmin):

    list_display = ('path', 'title', 'user', 'mark_date', 'is_valid')
    search_fields = ['path', 'title']
    date_hierarchy = 'mark_date'
    list_filter = ['user']

admin.site.register(PBlogEntry, PBlogEntryAdmin)
