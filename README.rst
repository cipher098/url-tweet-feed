url-tweets
==========

Twitter Stream microservice built using Django.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. You'll get email on provided id with a link to verify. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy url_tweets

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html


Local Setup
----------

1. Clone the Repository in your Local Machine
    $ git clone https://github.com/cipher098/url-tweet-feed.git
2. Create virtualenv.
6. cd url_tweets
3. Install requirements using command:
    $ pip install -r requirements/local.txt
4. Create .env file in url_tweets directory and add these variables with proper value:
::
    POSTGRES_HOST=localhost
    POSTGRES_DB=<db_name>
    POSTGRES_USER=<db_user>
    POSTGRES_PASSWORD=<db_password>
    CONN_MAX_AGE=<connection_max_age>

    EMAIL_HOST_USER=<email host for sending email>
    EMAIL_HOST_PASSWORD=<password for using smtp from email>

    TWITTER_CONSUMER_KEY=<twitter developer key>
    TWITTER_CONSUMER_SECRET_KEY=<twitter developer secret key>

5. Create db locally with the same details as provided in .env file.
    Steps: Run these commands in psql
::
    CREATE DATABASE <db_name>;
    CREATE ROLE <db_user> WITH LOGIN PASSWORD '<db_password>';
    ALTER ROLE <db_user> SET default_transaction_isolation TO 'read committed'
    GRANT ALL PRIVILEGES ON DATABASE <db_name> to <db_user>;
6. Run run server using command:
    python manage.py runserver



