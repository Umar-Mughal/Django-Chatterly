from utils.response_util import success_response, error_response


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
