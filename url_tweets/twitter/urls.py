from django.urls import path

from url_tweets.twitter.api import *

app_name = "twitter"
urlpatterns = [
    path("healthz/", view=health_check, name="health check"),
    path("tweets/", view=tweet_analyser, name="tweets"),
]
