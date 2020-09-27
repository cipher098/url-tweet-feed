from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TwitterConfig(AppConfig):
    name = 'url_tweets.twitter'
    verbose_name = _("Twitter")
