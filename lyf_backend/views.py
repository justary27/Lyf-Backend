from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, str(settings.BASE_DIR) + "/static/templates/index.html")


def handler500(request, *args, **argv):
    response = render(request, str(settings.BASE_DIR) + "/static/templates/500.html")
    response.status_code = 500
    return response


def handler404(request, exception):
    response = render(request, str(settings.BASE_DIR) + "/static/templates/404.html")
    print(exception)
    response.status_code = 404
    return response
