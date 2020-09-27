import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.template.response import TemplateResponse


from url_tweets.twitter.models import TwitterUserConfig, Tweet
from url_tweets.twitter.services import save_tweets, analyse_tweets
from url_tweets.twitter.twitter import TwitterAPI
import tweepy

import logging

logger = logging.getLogger(__name__)


def health_check(request):
    return HttpResponse(content="app is running", status=200)

@login_required(login_url='/accounts/login/') #redirect when user is not logged in
def tweet_analyser(request):
    oauth_token = request.GET.get('oauth_token', None)
    oauth_verifier = request.GET.get('oauth_verifier', None)

    user_id = request.user.id

    logger.info(f"Paramas recieved in request, oauth token: {oauth_token}, oauth verifier: {oauth_verifier}")

    twitter_user_config = TwitterUserConfig.objects.filter(user_id=user_id).first()
    twitter_api = TwitterAPI(twitter_user_config)

    if twitter_user_config is None:
        logger.info(f"TwitterUserConfig not found for current user, creating new.")
        twitter_user_config = TwitterUserConfig(
            user=request.user,
            oauth_token=twitter_api.auth.request_token['oauth_token'],
            oauth_token_secret=twitter_api.auth.request_token['oauth_token_secret'],
        )
        twitter_user_config.save()
        logger.info(f"Redirecting to: {twitter_api.authorization_url}")
        return HttpResponseRedirect(twitter_api.authorization_url)

    else:
        logger.info(f"TwitterUserConfig found for current user.")
        if twitter_user_config.access_token and twitter_user_config.access_token_secret:
            logger.info(f"Access token present in TwitterUserConfig.")
            twitter_api.set_access_token(
                access_token=twitter_user_config.access_token,
                access_token_secret=twitter_user_config.access_token_secret
            )
        else:
            try:
                twitter_api.get_access_token(oauth_verifier=oauth_verifier)
                twitter_user_config.access_token = twitter_api.auth.access_token
                twitter_user_config.access_token_secret = twitter_api.auth.access_token_secret
                twitter_user_config.save()

            except tweepy.error.TweepError:
                logger.info(f"Cannot get access token from oauth_verifier: {oauth_verifier}")
                twitter_user_config.hard_delete()
                twitter_api = TwitterAPI(twitter_user_config=None)
                twitter_user_config = TwitterUserConfig(
                    user=request.user,
                    oauth_token=twitter_api.auth.request_token['oauth_token'],
                    oauth_token_secret=twitter_api.auth.request_token['oauth_token_secret'],
                )
                twitter_user_config.save()
                logger.info(f"Redirecting to: {twitter_api.authorization_url}")
                return HttpResponseRedirect(twitter_api.authorization_url)

        tweets = twitter_api.get_tweets_with_url()
        save_tweets(tweets, user_id)
        response = analyse_tweets(user_id)

        return TemplateResponse(
            request, "tweets.html", response
        )
