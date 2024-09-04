from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from .models import Story, Tag, Comment, Like


# Create your views here.
@login_required
def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('sign_in')

    stories = Story.objects.order_by('-created_at')
    tags = Tag.objects.all()

    top_stories = Story.get_top_stories()[0:5]
    most_popular_tag = Tag.get_most_popular_tag()[:5]

    return render(request, 'post/index.html', {
        'stories': stories,
        'tags': tags,
        'top_stories': top_stories,
        'most_popular_tag': most_popular_tag
    })


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        tag = request.POST.getlist('tag')

        if not title or not content or not tag:
            return HttpResponse(status=400)

        story = Story.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        for t in tag:
            slug = slugify(t)
            tag, _ = Tag.objects.get_or_create(name=t, slug=slug)

            tag = tag.strip()

            story.tag.add(tag)

        story.save()

        return render(request, 'partials/post.html', {'story': story})


@login_required
def detail(request, story_id):
    story = Story.objects.get(id=story_id)

    tags = Tag.objects.all()

    top_stories = Story.get_top_stories()[0:5]
    most_popular_tag = Tag.get_most_popular_tag()[:5]

    return render(request, 'post/detail.html', {
        'story': story,
        'tags': tags,
        'top_stories': top_stories,
        'most_popular_tag': most_popular_tag
    })


def edit(request, story_id):
    pass


@login_required
def delete(request, story_id):
    user = request.user
    story = Story.objects.get(id=story_id)

    if user != story.author:
        return HttpResponse(status=403)

    story.delete()

    return HttpResponse("Story deleted")


def like(request, story_id):
    user = request.user

    try:
        like_ = Like.objects.create(
            user=user,
            story_id=story_id
        )

        like_.save()


    except Exception as e:
        like_ = Like.objects.get(
            user=user,
            story_id=story_id
        )

        like_.delete()

    return HttpResponse(f"<span id='story-like-{like_.story.id}'>{like_.story.get_like_count()}</span>")


def validate_title(request):
    title = request.POST.get('title', '').strip().replace(" ", "")

    if not title:
        return HttpResponse("<p id='error-title' style='color: red;'>Invalid Title</p>")

    story = Story.objects.filter(title=title).exists()


    if not title.isalpha():
        return HttpResponse("<p id='error-title' style='color: red;'>Invalid Title</p>")
    if story:
        return HttpResponse("<p id='error-title' style='color: red;'>Title already exists</p>")

    return HttpResponse("<p id='error-title' style='color: red;'></p>")


def validate_content(request):
    content = request.POST.get('content', '').strip()

    if not content:
        return HttpResponse("<p id='error-content' style='color: red;'>Invalid content</p>")


    if not content.isalpha():
        return HttpResponse("<p id='error-content' style='color: red;'>Invalid content</p>")

    return HttpResponse("<p id='error-content' style='color: red;'></p>")


def validate_tag(request):
    tag = request.POST.get('tag', '')

    if not tag.isalpha():
        return HttpResponse("<p id='error-tag' style='color: red;'>Invalid tag</p>")

    return HttpResponse("<p id='error-tag' style='color: red;'></p>")


@login_required
def comment(request, obj_id):
    if request.method == 'POST':
        content = request.POST.get('comment', '').strip()

        if not content:
            return HttpResponse(status=400)

        comment_ = Comment.objects.create(
            content=content,
            author=request.user,
            story_id=obj_id
        )

        print(comment_.content)

        comment_.save()

        return render(request, 'partials/comment.html', {'comment_': comment_})

    if request.method == 'DELETE':
        comment_ = Comment.objects.get(id=obj_id)
        comment_.delete()

        return HttpResponse("Comment deleted")


@login_required
def filter_(request, slug):
    tag = Tag.objects.get(slug=slug)
    stories = tag.stories.all()

    tags = Tag.objects.all()

    top_stories = Story.get_top_stories()[0:5]
    most_popular_tag = Tag.get_most_popular_tag()[:5]

    return render(request, 'post/filter.html',
                  {'stories': stories, 'tag': tag, 'tags': tags, 'top_stories': top_stories,
                   'most_popular_tag': most_popular_tag})
