from django.shortcuts import render

# Create your views here.


def index(request):
    """
    The index page

    :param request:
    :return:
    """
    ctx_data = {'ids': ['0', '1', '2', '3', '4', '5']}
    return render(request, 'covid/index.html', ctx_data)
