from django.shortcuts import render

# Create your views here.


def index(request):
    """
    The index page

    :param request:
    :return:
    """
    ctx_data = {}
    return render(request, 'covid/index.html', ctx_data)
