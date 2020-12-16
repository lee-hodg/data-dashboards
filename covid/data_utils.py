import pandas as pd
import plotly.graph_objs as go
# from google.oauth2 import service_account
import logging
import requests
import re
# import os
# import pandas_gbq

TODAY = pd.to_datetime('today')

logger = logging.getLogger(__name__)


def camel_to_title(input_str):
    """
    Convert a camelCase string to a title, e.g. someThing to Some Thing

    :param input_str:
    :return: titalized str
    """
    return ' '.join([s for s in re.split("([A-Z][^A-Z]*)", input_str) if s]).title()


def google_bq():
    """
    We could also fetch data from google big query covid set direct into pandas, but it is very slow
    to query in realtime
    :return:
    """
    # FIXME: takes too long. Consider an API like google Big Query
    # https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python
    # https://pandas-gbq.readthedocs.io/en/latest/
    # https://pandas-gbq.readthedocs.io/en/latest/howto/authentication.html
    # credentials = service_account.Credentials.from_service_account_file(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
    #
    # # TODO how can I get the actual data I want...namely confirmed cases grouped by country on latest date available
    # query = """
    # SELECT country_region, SUM(confirmed) num_reports
    # FROM `bigquery-public-data.covid19_open_data.compatibility_view`
    # GROUP BY country_region
    # HAVING num_reports IS NOT NULL
    # ORDER BY num_reports DESC
    # LIMIT 10
    # """
    #
    # df = pandas_gbq.read_gbq(query, project_id="covid-295815", credentials=credentials)

    return


def get_covid_data():
    """Fetch the covid data summary from the covid19api and do any cleaning

    Args:

    Returns:
        The cleaned pandas dataframe

    """
    logger.debug('Fetching Covid Data...')
    try:
        # resp = requests.get('https://api.covid19api.com/summary')
        resp = requests.get('https://corona.lmao.ninja/v2/countries')
        resp.raise_for_status()
    except requests.exceptions.RequestException as rexc:
        logger.error(rexc)
        return None, None
    logger.debug('Processing Covid Data...')

    df = pd.DataFrame(resp.json())

    # Clean it
    df.updated = pd.to_datetime(df.updated, unit='ms')
    return df


def get_historical_covid_data(country_names):
    """Fetch the covid historical data from the covid19api and do any cleaning

    Args:

    Returns:
        The cleaned pandas dataframe

    """
    logger.debug('Fetching Historical Covid Data...')
    try:
        resp = requests.get(f'https://corona.lmao.ninja/v2/historical/{country_names}?lastdays=all')
        resp.raise_for_status()
    except requests.exceptions.RequestException as rexc:
        logger.error(rexc)
        return None, None
    logger.debug('Processing Historical Covid Data...')

    # Cleaning
    # https://stackoverflow.com/questions/54537616/
    # flatten-dataframe-nested-list-array-with-extra-index-keys-for-time-series
    resp_json = resp.json()
    df = pd.DataFrame(resp.json())
    clean_df = pd.concat({k: pd.DataFrame(array) for k, array in df.pop('timeline').items()})
    clean_df = clean_df.reset_index(level=1).join(df).reset_index(drop=True)
    clean_df = clean_df.rename(columns={'level_1': 'date'})
    clean_df.date = pd.to_datetime(clean_df.date)

    return clean_df


def historical_graph(df, column_name='cases'):
    graph = []

    countrylist = df.country.unique().tolist()

    for country in countrylist:
        x_val = df[df['country'] == country].date.tolist()
        y_val = df[df['country'] == country][column_name].tolist()
        graph.append(
            go.Scatter(x=x_val,
                       y=y_val,
                       mode='lines',
                       name=country
                       )
        )

    layout = dict(title=f'Evolution of {column_name}',
                  xaxis=dict(title='Year',
                             autotick=True),
                  yaxis=dict(title=camel_to_title(column_name)),
                  )

    return graph, layout


def totals_graph(df, column_name='cases', top_n=10):
    """
    Bar plot of the total confirmed cases for the `top_10` countries

    Args:
        :param df: the pandas dataframe
        :param column_name: are we interested in TotalConfirmed or TotalDeaths for example
        :param top_n: how many countries to consider
    Returns:
        :return: the plot graph obj and layout and countries list
    """

    top_cases = df[['country', column_name]].sort_values(by=column_name, ascending=False)[0: top_n-1]\
        .reset_index(drop=True)

    graph = [go.Bar(x=top_cases.country.tolist(),
                    y=top_cases[column_name].tolist(),
                    )
             ]

    layout = dict(title=f'Top {top_n} countries by {camel_to_title(column_name)} ',
                  xaxis=dict(title='Country',),
                  yaxis=dict(title=camel_to_title(column_name)),
                  )

    return graph, layout, top_cases.country.tolist()


def return_figures():
    """Creates four plotly visualizations

    Args:

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    df = get_covid_data()
    graph_1, layout_1, top_cases_countries = totals_graph(df, column_name='cases', top_n=10)
    graph_2, layout_2, top_deaths_countries = totals_graph(df, column_name='deaths', top_n=10)
    graph_3, layout_3, _ = totals_graph(df, column_name='casesPerOneMillion', top_n=10)
    graph_4, layout_4, _ = totals_graph(df, column_name='deathsPerOneMillion', top_n=10)
    graph_5, layout_5, _ = totals_graph(df, column_name='testsPerOneMillion', top_n=10)


    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_1, layout=layout_1))
    figures.append(dict(data=graph_2, layout=layout_2))
    figures.append(dict(data=graph_3, layout=layout_3))
    figures.append(dict(data=graph_4, layout=layout_4))
    figures.append(dict(data=graph_5, layout=layout_5))


    return figures


def return_historical_figures():
    """Creates four plotly visualizations

    Args:

    Returns:
        list (dict): list containing the histriorical plotly visualizations

    """
    df = get_covid_data()
    _, _, top_cases_countries = totals_graph(df, column_name='cases', top_n=10)

    # Historical time series plots for top countries
    historical_df = get_historical_covid_data(','.join(top_cases_countries[:5]))
    graph_1, layout_1 = historical_graph(historical_df, column_name='cases')
    graph_2, layout_2 = historical_graph(historical_df, column_name='deaths')
    graph_3, layout_3 = historical_graph(historical_df, column_name='recovered')

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_1, layout=layout_1))
    figures.append(dict(data=graph_2, layout=layout_2))
    figures.append(dict(data=graph_3, layout=layout_3))

    return figures
