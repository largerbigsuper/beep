from django.shortcuts import render

from .tasks import task_add_blog_comment, task_add_blog_like, task_add_activity_commnet, task_add_user_following, task_add_user_following_after_create_blog
from django.http.response import HttpResponse
from beep.bot.tasks import task_add_blog_forward

def test_task_blog_add_commnet(request):
    task_add_blog_comment()
    return HttpResponse("test")

def test_task_add_blog_like(request):
    task_add_blog_like()
    return HttpResponse("test")

def test_task_add_blog_forward(request):
    task_add_blog_forward()
    return HttpResponse("test")

def test_task_add_activity_commnet(request):
    task_add_activity_commnet()
    return HttpResponse("test")

def test_task_add_user_following(request):
    task_add_user_following(1)
    return HttpResponse("test")

def test_task_add_user_following_after_create_blog(request):
    task_add_user_following_after_create_blog()
    return HttpResponse("test")

