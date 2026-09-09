from django.contrib import admin

from .models import Comment, Follow, Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Group)
