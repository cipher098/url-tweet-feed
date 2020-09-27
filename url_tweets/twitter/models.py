from dateutil import parser

from django.db import models

from url_tweets.utils.models import BaseModel
from url_tweets.users.models import User
import logging

logger = logging.getLogger(__name__)



class TwitterUserConfig(BaseModel):
    """
       TwitterUserConfig saves keys required for twitter authentication for user
    """

    user = models.OneToOneField(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        primary_key=True,
    )


    oauth_token = models.CharField(
        verbose_name='Oauth Token',
        null=False, blank=False,
        max_length=200,
    )

    oauth_token_secret = models.CharField(
        verbose_name='Oauth Token Secret',
        null=False, blank=False,
        max_length=200,
    )

    access_token = models.CharField(
        verbose_name='Access Token',
        null=True, blank=True,
        max_length=200,
    )

    access_token_secret = models.CharField(
        verbose_name='Access Token Secret',
        null=True, blank=True,
        max_length=200,
    )

    def __str__(self):
        return f"TwitterUserConfig "


class Tweet(BaseModel):
    """
    Selected fields from a Twitter Status object.
    Incorporates several fields from the associated User object.
    """

    class Meta:
        unique_together = (('user_id', 'tweet_id'),)


    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='tweets',
        null=True, blank=False, on_delete=models.CASCADE,
    )

    # Basic tweet info
    tweet_id = models.BigIntegerField()
    text = models.CharField(max_length=400)
    truncated = models.BooleanField(default=False)
    lang = models.CharField(max_length=9, null=True, blank=True, default=None)

    # Basic user info
    twitter_user_id = models.BigIntegerField()
    twitter_user_screen_name = models.CharField(max_length=50)
    twitter_user_name = models.CharField(max_length=150)
    twitter_user_verified = models.BooleanField(default=False)

    # Timing parameters
    user_utc_offset = models.IntegerField(null=True, blank=True, default=None)
    user_time_zone = models.CharField(max_length=150, null=True, blank=True, default=None)

    # Engagement - not likely to be very useful for now, but lets save it.
    favorite_count = models.PositiveIntegerField(null=True, blank=True)
    retweet_count = models.PositiveIntegerField(null=True, blank=True)
    user_followers_count = models.PositiveIntegerField(null=True, blank=True)
    user_friends_count = models.PositiveIntegerField(null=True, blank=True)

    # Relation to other tweets
    in_reply_to_status_id = models.BigIntegerField(null=True, blank=True, default=None)
    retweeted_status_id = models.BigIntegerField(null=True, blank=True, default=None)


    @classmethod
    def create_from_json(cls, raw):
        """
        Given a *parsed* json status object, construct a new Tweet model.
        """

        user = raw['user']
        retweeted_status = raw.get('retweeted_status')
        if retweeted_status is None:
            retweeted_status = {'id': None}

        # Replace negative counts with None to indicate missing data
        counts = {
            'favorite_count': raw.get('favorite_count'),
            'retweet_count': raw.get('retweet_count'),
            'user_followers_count': user.get('followers_count'),
            'user_friends_count': user.get('friends_count'),
        }
        for key in counts:
            if counts[key] is not None and counts[key] < 0:
                counts[key] = None

        tweet = cls(
            # Basic tweet info
            tweet_id=raw['id'],
            text=raw['text'],
            truncated=raw['truncated'],
            lang=raw.get('lang'),

            # Basic user info
            twitter_user_id=user['id'],
            twitter_user_screen_name=user['screen_name'],
            twitter_user_name=user['name'],
            twitter_user_verified=user['verified'],

            # Timing parameters
            created=parser.parse(raw['created_at']),
            user_utc_offset=user.get('utc_offset'),
            user_time_zone=user.get('time_zone'),

            # Engagement - not likely to be very useful for streamed tweets but whatever
            favorite_count=counts.get('favorite_count'),
            retweet_count=counts.get('retweet_count'),
            user_followers_count=counts.get('user_followers_count'),
            user_friends_count=counts.get('user_friends_count'),

            # Relation to other tweets
            in_reply_to_status_id=raw.get('in_reply_to_status_id'),
            retweeted_status_id=retweeted_status['id']
        )
        return tweet


class Link(BaseModel):
    """
    Saves links present in Tweet.
    """

    tweet = models.ForeignKey(
        Tweet,
        verbose_name='Tweet',
        related_name='links',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    url = models.CharField(max_length=400, null=False, blank=True)

    domain = models.CharField(max_length=200, null=False, blank=True)

