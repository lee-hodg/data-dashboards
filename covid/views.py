from django.shortcuts import render
from .data_utils import return_figures, return_historical_figures
from django.views.decorators.cache import cache_page

import json
import plotly

# Create your views here.


@cache_page(60 * 60)
def index(request):
    """
    The index page

    :param request:
    :return:
    """

    figures = return_figures()

    # plot ids for the html id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    ctx_data = {'ids': ids,
                'figuresJSON': figures_json}

    return render(request, 'covid/index.html', ctx_data)


@cache_page(60 * 60)
def history(request):
    """
    The history page

    :param request:
    :return:
    """

    figures = return_historical_figures()

    # plot ids for the html id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figures_json = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    ctx_data = {'ids': ids,
                'figuresJSON': figures_json}

    return render(request, 'covid/history.html', ctx_data)
