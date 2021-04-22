# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse

# Local Django
from posts.forms import CommentForm, PostForm
from posts.models import Category, Post


def home_page(request, category=None):
    """Mutual view for all posts and search results.

    On GET request all post will show up, if the GET request made using the
    search bar, posts will be filtred according to the entered search query.

    Keyword Arguments:
        category {str} -- Search query (default: {None})

    Returns:
        Queryset -- Either all posts or the filtered posts according to the
        search query.
    """

    title = 'Home page'
    posts = Post.objects.all()

    # Filter by category.
    if category:
        posts = Post.objects.filter(categories__name__icontains=category)

    # Search results.
    query = request.GET.get('query')
    if query and not query.isspace():
        # Change page title.
        title = 'Search results'
        # Get related query posts.
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Pagination.
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # Last page.
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'posts': paginated_queryset,
        'categories': Category.objects.all(),
        #   If posts are related to search query. Paginate the search results
        # using the query as a string parameter
        'query': query
    }

    return render(request, 'home.html', context)


def post_details(request, id):
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


@login_required(login_url="accounts:signin")
def post_form(request, id=None):
    """ Create/Update/Delete post."""

    context = {
        'categories': Category.objects.all(),
        'title': None,
        'form': None,
        'post': None,
    }

    try:
        author = request.user.author

        # If user is an author
        if author:
            # Post model CRUD operations.
            # Delete request.
            if request.resolver_match.url_name == 'post_delete':
                post = get_object_or_404(Post, id=id)
                messages.success(request, f'{post.title} deleted.')
                post.delete()
                return redirect('post_home_page')
            # NOTE: Both Update and Create request related to the same HTML.
            # Update request with model instance for the form.
            elif request.resolver_match.url_name == 'post_update':
                context['title'] = 'Update post'
                post = get_object_or_404(Post, id=id)
                form = PostForm(request.POST or None, instance=post)
                # Next to general render.
            # Create request with regular form.
            elif request.resolver_match.url_name == 'post_create':
                context['title'] = 'Create new post'
                form = PostForm(request.POST or None)
                # Next to general render.

            # Form actions associated with Update and Create requests.
            if request.method == 'POST':
                if form.is_valid():
                    form.instance.author = author
                    form.save()
                    messages.success(request, f'{form.instance.title} Created')
                    return redirect(
                        reverse('post_details', kwargs={
                                'id': form.instance.id})
                    )

            # General render. Mutual between Create and Update.
            context['form'] = form
            return render(request, 'create-post.html', context)

    # If user is not an author.
    except Exception as e:
        messages.warning(request, e)
        return redirect('post_home_page')


def post_comment_create(request, id):
    post = Post.objects.get(pk=id)

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

    else:
        messages.warning(request, 'Post does not exist.')
        return redirect('post_home_page')

    context = {
        'categories': Category.objects.all(),
        'post': post,
    }

    return render(request, 'post-details.html', context)
