from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect

# from ...models import BlogPost
from utils.helpers import success_response, error_response
import pprint


def index(request):
    content = "<html><body><h1>Hello, World!</h1></body></html>"
    content_type = "text/html"
    status = 200
    reason = "OK"
    charset = "utf-8"
    headers = {"X-Custom-Header": "Custom Value", "Cache-Control": "no-cache"}
    response = HttpResponse(
        content=content,
        content_type=content_type,
        status=status,
        reason=reason,
        charset=charset,
        headers=headers,
    )
    return response


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            # BlogPost.objects.create(title=title, content=content)
            return success_response("data is inserted successfully")
        else:
            return error_response("title or content is missing")
    else:
        return error_response("http method is wrong")
