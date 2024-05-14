from django.http import JsonResponse


def success_response(message="", data={}, status=200):
    return JsonResponse({"success": True, "message": message, "data": data}, status)


def error_response(message="", data={}, status=400):
    return JsonResponse(
        {"success": False, "message": message, "data": data}, status=status
    )
