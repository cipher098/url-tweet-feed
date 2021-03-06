url-tweets
==========

Twitter Stream microservice built using Django. It gets all tweets of user/friends which are having URL or media(image, video) in it.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT

Live Demo
--------------
    :Demo: https://url-tweet-feed.herokuapp.com/


How to Use?
----------
::
    1. Go to home page.
    2. Sign up, if not done already. Will have to confirm email using a link which will come to email.
    3. Sign In.
    4. Click on Twitter from Nav Bar.
    5. First time, you would redirected to twitter to authorize us.
    6. Voylla, app is ready for you. Enjoy!



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
2. Create virtualenv
::
    $ virtualenv -p $(which python3) url_tweets
    $ source url_tweets/bin/activate
3. Go to project directory:
    $ cd url_tweets
4. Install requirements using command:
    $ pip install -r requirements/local.txt
5. For sending email using gmail smtp setup will be required, follow first 3 steps in this link to do setup in gmail:
    :Tutorial: https://support.cloudways.com/configure-gmail-smtp/
6. To run this project twitter developer keys will be required, if you're not having them please apply for them before proceeding to steps below.
7. Create .env file in url_tweets directory and add these variables with proper value:
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

8. Create db locally with the same details as provided in .env file. Run these commands in psql:
::
    $ CREATE DATABASE <db_name>;
    $ CREATE ROLE <db_user> WITH LOGIN PASSWORD '<db_password>';
    $ ALTER ROLE <db_user> SET default_transaction_isolation TO 'read committed'
    $ GRANT ALL PRIVILEGES ON DATABASE <db_name> to <db_user>;
9. Apply migrations to db using command:
    python manage.py migrate

10. Run server using command:
    python manage.py runserver



