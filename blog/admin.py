from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Contact, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'preview', 'created_at', 'is_published']
    search_fields = ['title']

    def preview(self, obj):
        return format_html(f"<img height=50 width=50 src='{obj.image.url}'>")


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_solved']
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'email', 'created_at']
    search_fields = ['name']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Comment, CommentAdmin)
