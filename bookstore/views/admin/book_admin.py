from django.contrib import admin
from django.utils.html import format_html

class BookAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'author', 'price', 'category', 'stock', 'status')
    search_fields = ('title', 'author', 'category',)
    list_filter = ('author', 'category', 'status')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.imagePath.url))
