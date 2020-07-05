from django.shortcuts import render

from .tasks import task_add_blog_commnet, task_add_blog_like
from django.http.response import HttpResponse
from beep.bot.tasks import task_add_blog_forward

def test_task_blog_add_commnet(request):
    task_add_blog_commnet()
    return HttpResponse("test")

def test_task_add_blog_like(request):
    task_add_blog_like()
    return HttpResponse("test")

def test_task_add_blog_forward(request):
    task_add_blog_forward()
    return HttpResponse("test")

