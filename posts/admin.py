from django.contrib import admin

from .models import Post, Group, Comment, Follow


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'description',
        'created',
        'author_id'
    )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('slug', )
    empty_value_display = '-пусто-'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group'
    )
    search_fields = ('text', 'group')
    list_filter = ('pub_date', 'group')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'post',
        'author',
        'created'
    )
    search_fields = ('text', 'author')
    list_filter = ('created', 'post')
    empty_value_display = '-пусто-'


class FollowForm(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author'
    )
    search_fields = ('user', 'author')
    list_filter = ('id',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowForm)
