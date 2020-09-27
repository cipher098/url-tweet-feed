from datetime import datetime, timedelta
from django.utils import timezone
import tldextract

from django.db.models import Count

import logging

logger = logging.getLogger(__name__)

from url_tweets.twitter.models import TwitterUserConfig, Tweet, Link


def save_tweets(tweets, user_id):
    tweet_objects = []
    link_objects = []
    min_time = timezone.now() - timedelta(days=7)
    existing_tweet_ids = Tweet.objects.filter(user_id=user_id, created__gte=min_time).values_list('tweet_id', flat=True)
    saved_tweets = 0
    for tweet in tweets:
        if tweet._json['id'] not in existing_tweet_ids:
            saved_tweets += 1
            tweet_object = Tweet.create_from_json(tweet._json)
            tweet_object.user_id = user_id
            tweet_objects.append(tweet_object)

            links_in_tweet = tweet._json['entities']['urls']
            for link in links_in_tweet:
                url = link['expanded_url']
                domain = tldextract.extract(url).domain
                link_object = Link(
                    url=url,
                    tweet=tweet_object,
                    domain=domain
                )
                link_objects.append(link_object)

    Tweet.objects.bulk_create(tweet_objects)
    Link.objects.bulk_create(link_objects)
    logger.info(f"Saved: {saved_tweets} tweets out of {len(tweets)} tweets.")


def analyse_tweets(user_id):
    """
        Provides analysis of last 7 days of tweets:
            which domain is most tweeted by friends/user
            which user tweeted most links
    """
    min_time = timezone.now() - timedelta(days=7)
    tweets = Tweet.objects.filter(user_id=user_id, created__gte=min_time)
    links = Link.objects.filter(tweet__in=tweets)

    tweet_texts = list(tweets.values('text', 'tweet_id'))
    tweet_links_domain_count = None
    max_links_shared_by = None
    if len(links):
        tweet_links_domain_count = links.values('domain').annotate(total=Count('domain')).order_by('-total')

        max_links_shared_by = tweets.values('twitter_user_id', 'twitter_user_screen_name').annotate(total=Count('links')).order_by('-total')[0]

    response = {
        'tweets': tweet_texts,
        'tweet_links_domain_count': tweet_links_domain_count,
        'max_links_shared_by': max_links_shared_by
    }

    return response

