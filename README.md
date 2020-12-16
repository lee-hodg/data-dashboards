# Environment variables

The following environment variables are required for this project

- `DJANGO_SECRET_KEY`: the Django secret key
- `DJANGO_RUNTIME_ENVIRONMENT`: are we local-dev, staging or production?

The key can be generated with the command

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
## Local management

For local development I use [direv](https://direnv.net/) to set these variables. 
After installing the `direnv` hook to zsh (or your shell of choice) this amounts to including 
a `.envrc` file in the project root directory and running `direnv allow`.

# Package management

[Poetry](https://python-poetry.org/docs/) is used to manage dependencies.

To set up the existing project for poetry first execute

```python
poetry init
```

This will generate the `pyproject.toml` file, with the dependencies and dev dependencies

For convenience during development we also have the following dev dependencies

```python
django-debug-toolbar
coloredlogs
Werkzeug
django-extensions
```

Next run 

```
poetry install
```

Adding and removing packages with poetry:

```bash
poetry add X --dev # dev only
poetry add Y  # non -dev
poetry remove Z  # remove
```

Updating

```bash
poetry update X
```

Generating a regular `requirements.txt`

```bash
poetry export -f requirements.txt > requirements.txt --without-hashes
```

The location of the virtualenv set up by poetry can be found by running

```bash
poetry config --list 
```

# Configuring IntelliJ

To set up the Python environment go to `File>Project Structure`

Now under `Platform Settings> SDKs` click the `+` symbol and choose `Add Python SDK`.
Select the existing environment bullet and locate the `bin/python/python3.8` binary. 
Finally, click OK

Now under `Project Settings` of the same modal popup select the SDK you just added 
under `Project SDK` and click `Apply`.

# Database migrations

Ensure to run

```bash
python manage.py migrate
```

if this is the first use.


# Local development runserver and shell

For local development `Django-Debug-Toolbar` is available for aid in debugging the app.
You should see colored logging and `runserver_plus` and `shell_plus` available
via [django-extensions](https://django-extensions.readthedocs.io/). 

You can start these with

```bash
python manage.py runserver_plus
python manage.py shell_plus
```

# Bootstrap

In this project we use [django-bootstrap](https://django-bootstrap4.readthedocs.io/en/latest/quickstart.html)

# Deploying on Heroku

The project uses [whitenoise](http://whitenoise.evans.io/en/stable/) for self-serving on static files
This involved adding the package with Poetry and then adding to the Django Middleware

```python
MIDDLEWARE = [
  # 'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
]

We also use the [django-heroku](https://github.com/heroku/django-heroku) to care of a bunch
of things like `ALLOWED_HOSTS` and static files settings.

```
Create the app on Heroku

```bash
heroku create
```

Set some environment variables

```bash
heroku config:set DJANGO_SECRET_KEY="XXXX"
heroku config:set DJANGO_RUNTIME_ENVIRONMENT="production"
```

Now deploy with

```bash
git push heroku master
```

## Provision memcached

```bash
heroku addons:create memcachier:dev
```

Then add the `CACHES` code from the [heroku docs](https://devcenter.heroku.com/articles/django-memcache)

Followed by

```bash
sudo apt-get install libmemcached-dev
poetry add pylibmc==1.5.2
poetry export -f requirements.txt > requirements.txt --without-hashes
```
