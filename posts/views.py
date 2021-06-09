# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
# Local apps
from posts.forms import CommentForm, PostForm
from posts.helpers import pagination
from posts.models import Category, Notification, Post


@require_GET
def post_list(request, category=None):
    posts = Post.objects.only('id', 'thumbnail', 'title', 'created_time')

    context = {
        'title': 'Home page',
        'posts': pagination(request, posts, 6),
        'categories': Category.objects.all(),
    }

    return render(request, 'post-list.html', context)


@require_GET
def post_filter_by_category(request, category=None):
    posts = Post.objects.only('id', 'thumbnail', 'title', 'created_time')

    if category:
        posts = Post.objects.filter(categories__name__icontains=category)\
            .only('id', 'thumbnail', 'title', 'created_time')

    context = {
        'title': f'{category} posts',
        'posts': pagination(request, posts, 6),
        'categories': Category.objects.all(),
    }

    return render(request, 'post-list.html', context)


@require_GET
def post_search(request):
    posts = Post.objects.only('id', 'thumbnail', 'title', 'created_time')

    query = request.GET.get('query')
    # Query is not just space characters.
    if query and not query.isspace():
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    print(query)

    context = {
        'title': 'Search results',
        'posts': pagination(request, posts, 6),
        'categories': Category.objects.all(),
        # Passing query value in the HttpResponse, to receive it with the
        # HttpRequest so that it be possible to paginate the search results.
        # -- refer to includes/paginator.html --
        'query': query
    }

    return render(request, 'post-list.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url="accounts_login")
def post_create(request):
    """
    Allow Author to create post.
    """
    try:
        author = request.user.author

        form = PostForm(request.POST or None)
        if request.method == 'POST':
            form.instance.author = author
            if form.is_valid():
                form.save()
                messages.success(request, f'{form.instance.title} Created')
                return redirect(
                    reverse('post_details', kwargs={'id': form.instance.id})
                )

        context = {
            'title': 'Create Post.',
            'categories': Category.objects.all(),
            'form': form,
        }

        return render(request, 'post-create.html', context)

    except ObjectDoesNotExist:
        messages.warning(request, 'Not authorized.')
        return redirect('post_list')


@require_http_methods(["GET", "POST"])
@login_required(login_url="accounts_login")
def post_update(request, id):
    """
    Allow Author to update post.
    """
    try:
        author = request.user.author

        post = Post.objects.get(id=id)
        form = PostForm(request.POST or None, instance=post)
        if request.method == 'POST':
            form.instance.author = author
            if form.is_valid():
                form.save()
                messages.success(request, f'{form.instance.title} updated.')
                return redirect(
                    reverse('post_details', kwargs={'id': form.instance.id})
                )

        context = {
            'title': 'Create Post.',
            'categories': Category.objects.all(),
            'form': form,
        }

        return render(request, 'post-create.html', context)

    except ObjectDoesNotExist:
        messages.warning(request, 'Not authorized.')
        return redirect('post_list')


@require_GET
@login_required(login_url="accounts_login")
def post_delete(request, id):
    """
    Allow Author to delete post.
    """
    try:
        request.user.author

        post = get_object_or_404(Post, id=id)
        messages.success(request, f'{post.title} deleted.')
        post.delete()
        return redirect('post_list')

    except ObjectDoesNotExist:
        messages.warning(request, 'Not authorized.')
        return redirect('post_list')


@require_GET
def post_details(request, id):
    post = get_object_or_404(Post, id=id)

    context = {
        'categories': Category.objects.all(),
        'post': post,
    }

    return render(request, 'post-details.html', context)


@require_GET
@login_required(login_url="accounts_login")
def post_related_to_author(request):
    author = request.user.author
    posts = Post.objects.filter(author=author).only('id', 'title')

    if posts.exists():
        context = {
            'posts': pagination(request, posts, 6),
            'categories': Category.objects.all()
        }
        return render(request, 'post-list.html', context)
    else:
        return redirect(reverse('post_list'))


@require_POST
@login_required(login_url="accounts_login")
def comment_create(request, id):
    post = get_object_or_404(Post, pk=id)
    form = CommentForm(request.POST)
    form.instance.post = post
    form.instance.content = request.POST.get('content')
    if form.is_valid():
        form.save()
        messages.success(request, 'Thanks for your comment!!.')
        return redirect(reverse('post_details', kwargs={'id': post.id}))
    else:
        messages.warning(request, 'Sorry, something went wrong!!.')
        return redirect(post_list)


@require_GET
@login_required(login_url="accounts_login")
def notification_list(request):
    """
    List current notifications related to current logged-in Author.
    """
    try:
        author = request.user.author.id
        notifications = Notification.objects.select_related('post').\
            filter(post__author=author)
        if notifications.exists():
            title = 'Notifications'
            notifications = pagination(request, notifications, 20)
        else:
            title = 'No notifications'
            notifications = None

    # Logged-in User not an Author
    except ObjectDoesNotExist:
        pass

    context = {
        'title': title,
        'notifications': notifications
    }

    return render(request, 'notifications.html', context)


@require_GET
def notification_details(request, id):
    notification = Notification.objects.get(id=id)
    notification.viewed = True
    notification.save()

    return redirect(notification.get_absolute_url())
