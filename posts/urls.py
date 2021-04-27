from django.urls import path

from . import views


urlpatterns = [
    path(
        'group/<slug:slug>/group_edit/',
        views.group_edit, name='group_edit'
    ),
    path(
        'add_group/',
        views.add_group, name='add_group'
    ),
    path('new/', views.new_post, name='new_post'),
    path(
        "follow/", views.follow_index, 
        name="follow_index"
    ),
    path(
        "<username>/<int:post_id>/<int:comment_id>/comment_edit",
        views.comment_edit,
        name="comment_edit"
    ),
    path(
        'search_by_text/',
        views.search_by_text,
        name='search_by_text'
    ),
    # path(
    #     "group/<slug:slug>/unfollow/",
    #     views.group_unfollow, name="group_unfollow"
    # ),
    # path(
    #     'group/<slug:slug>/follow/',
    #     views.group_follow, name='group_follow'
    # ),
    path(
        "<str:username>/unfollow/",
        views.profile_unfollow, name="profile_unfollow"
    ),
    path(
        '<str:username>/follow/',
        views.profile_follow, name='profile_follow'
    ),
    path(
        '<str:username>/<int:post_id>/', 
        views.post_view, name='post'
    ),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit, name='post_edit'
    ),

    path(
        'group/<slug:slug>/',
        views.posts_group, name='posts_group'
    ),

    path(
        "<username>/<int:post_id>/comment",
        views.add_comment,
        name="add_comment"
    ),
    path(
        '<str:username>/', views.profile, 
        name='profile'
    ),
    path('', views.index, name='index'),
]
