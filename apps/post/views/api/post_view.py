from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect

from utils.helpers import success_response, error_response
import pprint


def create_post_v1(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # BlogPost.objects.create(title=title, content=content)
            return success_response("data is inserted successfully")
        else:
            return error_response("title or content is missing")
    else:
        return error_response("http method is wrong")
