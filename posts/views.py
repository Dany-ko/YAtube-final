from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Post, Group, User, Follow, Comment
from .forms import PostForm, CommentForm, GroupForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator
    }
    return render(
        request, 'index.html',
        context
    )


def page_not_found(request, exception):
    return render(
        request, 'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request, 'misc/500.html',
        status=500
    )


@login_required
def add_group(request):
    if not request.method == 'POST':
        form = GroupForm()
        return render(request, 'add_group.html', {'form': form}) 
    form = GroupForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'add_group.html', {'form': form})
    group = form.save(commit=False)
    group.author = request.user
    group.save()
    return redirect(
        'posts_group', group.slug
    )


def group_edit(request, slug):
    group = get_object_or_404(
        Group, slug=slug
    )
    if request.user.username != group.author.username:
        return redirect(
            'posts_group',
            slug=slug,
        )
    form = GroupForm(
        request.POST or None, 
        files=request.FILES or None, 
        instance=group
    )
    if not form.is_valid():
        context = {
            'form': form, 'group': group,
            'group_edit': 'group_edit'
        }
        return render(request, 'add_group.html', context)
    group.save()
    return redirect(
        'posts_group',
        slug=slug
    )


def posts_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group, 'page': page,
        'paginator': paginator
    }
    return render(request, 'group.html', context)


@login_required
def new_post(request):
    if not request.method == 'POST':
        form = PostForm()
        return render(request, 'new.html', {'form': form}) 
    form = PostForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'new.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(
        User, username=username
    )
    following = author.following.filter(
        user=request.user.id
    )
    follower = author.follower.filter(
        user=request.user.id
    )
    post_list = author.users.all()
    paginator = Paginator(post_list, 10)
    page_namber = request.GET.get('page')
    page = paginator.get_page(page_namber)
    context = {
        'page': page, 'paginator': paginator,
        'count': post_list.count, 'author': author,
        'following': following, 'follower': follower
    }
    return render(request, 'profile.html', context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(
            Post, author__username=username,
            id=post_id
        )
    if not request.method == 'POST':
        form = CommentForm()
        return redirect('post', username, post_id)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return redirect('post', username, post_id)
    comment = form.save(commit=False) 
    comment.author = request.user
    comment.post = post
    comment.save()
    return redirect('post', username, post_id)


@login_required
def comment_edit(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.username != comment.author.username:
        return redirect('post', username, post_id)
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None,
        instance=comment
    )
    if not form.is_valid():
        context = {
            'form': form, 'comment': comment,
        }
        return render(request, 'post.html', context)
    form.save()
    return redirect('post', username, post_id,)


def post_view(request, username, post_id):
    post = get_object_or_404(
        Post, author__username=username,
        id=post_id
    )
    comments = Comment.objects.filter(post=post)
    user_comments = Comment.objects.filter(
        author__username=request.user.username,
        post=post
    )
    user_comments_forms = []
    for form in user_comments:
        user_comments_forms.append(CommentForm(
            request.POST or None,
            files=request.FILES or None,
            instance=form
        ))
    posts_count = post.author.users.count()
    form = CommentForm()
    context = {
        'post': post, 'count': posts_count,
        'author': post.author, 'form': form,
        'comments': comments,
        'user_comments_forms': user_comments_forms
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = Post.objects.get(
        author__username=username, id=post_id
    )
    if request.user.username != username:
        return redirect(
            'post',
            username=username,
            post_id=post.id,
        )
    form = PostForm(
        request.POST or None, 
        files=request.FILES or None, 
        instance=post
    )
    if not form.is_valid():
        context = {
            'form': form, 'post': post,
            'post_edit': 'post_edit'
        }
        return render(request, 'new.html', context)
    post.save()
    return redirect(
        'post',
        username=username,
        post_id=post.id,
    )


@login_required
def follow_index(request):
    post_list = Post.objects.filter(
        author__following__user=request.user
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 
        'paginator': paginator
    }
    return render(request, "follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(
            author=author, user=request.user
        )
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        following = Follow.objects.filter(
            author=author,
            user=request.user
        ).exists()
        if following == True:
            Follow.objects.get(
            author=author,
            user=request.user
        ).delete()
    return redirect('profile', username)


# @login_required
# def group_follow(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     if group.slug != slug:
#         Follow.objects.get_or_create(
#             slug=slug, user=request.user
#         )
#     return redirect('posts_group', slug)


# @login_required
# def group_unfollow(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     if group.slug != slug:
#         following = Follow.objects.filter(
#             slug=slug,
#             user=request.user
#         ).exists()
#         if following == True:
#             Follow.objects.get(
#             slug=slug,
#             user=request.user
#         ).delete()
#     return redirect('posts_group', slug)


# class SearchResultView(ListView):
#     model = Post
#     template_name = 'search_result.html'


def search_by_text(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(text__contains=search_query)
        context = {
            'posts': posts,
            'search_query': search_query
        }
        return render(request, 'index.html', context)
