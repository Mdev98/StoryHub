from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from authentication.models import User
from post.models import Story


# Create your views here.

@login_required
def profile(request, username):
    user_id = User.objects.get(username=username).id
    stories = Story.objects.filter(author=user_id)
    likes_count = 0
    story_count = stories.count()
    for story in stories:
        likes_count = story.get_like_count()

    #  get the most liked story from the user stories
    top_story = Story.get_top_stories().filter(author=user_id).first()
    print(top_story)

    return render(request, 'account/profile.html',
                  {'stories': stories, 'likes_count': likes_count, 'story_count': story_count, 'top_story': top_story})


def settings(request):
    return render(request, 'account/settings.html')


def update_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if first_name and validate_name(first_name):
            request.user.first_name = first_name
            request.user.save()

            return HttpResponse(first_name)
        elif last_name and validate_name(last_name):
            request.user.last_name = last_name
            request.user.save()

            return HttpResponse(last_name)

    return HttpResponse('Invalid input')


def update_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        if not validate_password(password):
            return HttpResponse('Password must be at least 8 characters long')

        request.user.set_password(password)
        request.user.save()

    return HttpResponse('Password updated')


def validate_password(password):
    if len(password) < 8:
        return False
    return True


def validate_name(name):
    if name.isalpha():
        return True
    return False
