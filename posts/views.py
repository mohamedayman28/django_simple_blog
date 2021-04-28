# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponse

# Local apps
from posts.forms import CommentForm, PostForm
from posts.helper import pagination
from posts.models import Category, Post


def home_page(request, category=None):
    """List posts and filter on Query String or Keyword.

    On GET request List all posts.
    If GET request made from the search bar, filter and list posts by query
    string.
    If GET request made with URL captured value EX:<category>, filter and list
    posts by query string.

    Keyword Arguments:
        category {str} -- URL captured value EX:<category> (default: {None})

    Returns:
        Queryset -- Post objects within home.html.
    """

    title = 'Home page'
    posts = Post.objects.only('id', 'thumbnail', 'title', 'timestamp')

    # If request has category argument, filter using that argument.
    if category:
        posts = Post.objects.filter(categories__name__icontains=category)\
            .only('id', 'thumbnail', 'title', 'timestamp')

    query = request.GET.get('query')

    # If GET request from search bar
    if query and not query.isspace():
        title = 'Search results'
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    context = {
        'title': title,
        'posts': pagination(request, posts, 6),
        'categories': Category.objects.all(),
        # Passing query value in the response to receive it with the request so
        # that it be possible to paginate the filtered queryset.
        # -- refer to includes/paginator.html --
        'query': query
    }

    return render(request, 'home.html', context)


def post_details(request, id):
    """
    Arguments:
        id {int} -- Get post with its id.

    Returns:
        Object -- Post object within post-details.html.
    """

    try:
        post = Post.objects.get(id=id)
    except (Post.DoesNotExist, ValueError):
        messages.warning(request, 'Post does not exist.')
        return redirect('post_home_page')

    context = {
        'categories': Category.objects.all(),
        'post': post,
    }

    return render(request, 'post-details.html', context)


@login_required(login_url="accounts_login")
def author_posts(request):
    """List posts related to an author.

    On GET request, If user:
        Not logged-in redirect to login page.
        Logged-in but is not an author, redirect to the home page.
        Logged-in and is an author, list posts related to that user.

    Decorators:
        login_required
    """

    author = request.user.author
    posts = Post.objects.filter(author=author).only('id', 'title')

    # If at least one result exists
    if posts.exists():
        context = {
            'posts': pagination(request, posts, 6),
            'categories': Category.objects.all()
        }
        return render(request, 'author-posts.html', context)
    else:
        return redirect(reverse('post_home_page'))


@login_required(login_url="accounts_login")
def post_form(request, id=None):
    """Create/Update/Delete post.

    If user is not an author redirect ot home page.
    If user is an author they can Create/Update/Delete related post objects.

    Decorators:
        login_required

    Keyword Arguments:
        id {int} -- Get post with its id (default: {None}).

    Returns:
        Object -- Post object within post-details.html.
    """

    context = {
        'categories': Category.objects.all(),
        'title': None,
        'form': None,
        'post': None,
    }

    # Make sure request made by an author.
    try:
        author = request.user.author

        # If user is an author, they have the option to CRUD on related post.
        if author:
            url_name = request.resolver_match.url_name

            # Delete request.
            if url_name == 'post_delete':
                post = get_object_or_404(Post, id=id)
                messages.success(request, f'{post.title} deleted.')
                post.delete()
                return redirect('post_home_page')

            # Update request with model instance for the form.
            elif url_name == 'post_update':
                context['title'] = 'Update post'
                post = get_object_or_404(Post, id=id)
                form = PostForm(request.POST or None, instance=post)
                # Next: Handle the form. Then: Render create-post.html.

            # Create request with regular form.
            elif url_name == 'post_create':
                context['title'] = 'Create new post'
                form = PostForm(request.POST or None)
                # Next: Handle the form. Then: Render create-post.html.

            # Mutual form behavior between Update and Create post.
            if request.method == 'POST':
                if form.is_valid():
                    form.instance.author = author
                    form.save()
                    messages.success(request, f'{form.instance.title} Created')
                    return redirect(
                        reverse('post_details', kwargs={
                                'id': form.instance.id})
                    )

            context['form'] = form
            return render(request, 'create-post.html', context)

    # If user is not an author.
    except Exception as e:
        messages.warning(request, e)
        return redirect('post_home_page')


def post_comment_create(request, id):
    """Create comment related to post object.

    Arguments:
        id {int} -- Get post with its id.
    """
    try:
        post = get_object_or_404(Post, pk=id)

        if request.method == 'POST':
            form = CommentForm(request.POST)
            # Populate form instance.
            form.instance.commenter = request.user
            form.instance.post = post
            form.instance.content = request.POST.get('content')

            if form.is_valid():
                form.save()
                messages.success(request, 'Thanks for your comment!!.')
                return redirect(reverse('post_details', kwargs={'id': post.id}))

    # On GET request attempt, or the post object does not exist.
    except:
        messages.warning(request, 'Post does not exist.')
        return redirect('post_home_page')

    context = {
        'categories': Category.objects.all(),
        'post': post,
    }

    return render(request, 'post-details.html', context)
