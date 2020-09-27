import tweepy
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


class TwitterAPI:
    def __init__(self, twitter_user_config=None):
        self.auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                                        settings.TWITTER_CONSUMER_SECRET_KEY,
                                        settings.BASE_URL + "/twitter/tweets")

        if twitter_user_config:
            oauth_token_secret = twitter_user_config.oauth_token_secret
            oauth_token = twitter_user_config.oauth_token
            access_token = twitter_user_config.access_token
            access_token_secret = twitter_user_config.access_token_secret
        else:
            oauth_token_secret = None
            oauth_token = None
            access_token = None
            access_token_secret = None

        if access_token and access_token_secret:
            self.set_access_token(access_token, access_token_secret)
        else:
            if oauth_token_secret is None or oauth_token is None:
                self.authorization_url = self.auth.get_authorization_url()
            else:
                self.auth.request_token['oauth_token_secret'] = oauth_token_secret
                self.auth.request_token['oauth_token'] = oauth_token

        self.client = tweepy.API(self.auth)



    def get_access_token(self, oauth_verifier):
        self.auth.get_access_token(oauth_verifier)

    def set_access_token(self, access_token, access_token_secret):
        self.auth.set_access_token(access_token, access_token_secret)

    def get_required_users(self):
        """Returns list containing user name of user and his friends."""
        required_users = [self.client.me().screen_name]
        friends = self.client.friends()
        required_users.extend([friend.screen_name for friend in friends])
        return required_users


    def get_tweets_with_url(self):
        """Gets tweets which are having URL or media"""
        required_users = self.get_required_users()
        # query_string = f"from:{' OR from:'.join(required_users)} filter:links -is:retweets -filter:images -filter:videos -filter:midea url:https -url:https://twitter.com"
        # query_string = f"from:{' OR from:'.join(required_users)} filter:links url:https -url:https://twitter.com -filter:images -filter:videos -filter:retweets"
        # query_string = f"from:{' OR from:'.join(required_users)} filter:links url:https -filter:images -filter:videos -filter:retweets -url:https://www.twitter.com"
        query_string = f"from:{' OR from:'.join(required_users)} filter:links url:https -filter:retweets -url:https://www.twitter.com"
        tweets = self.client.search(q=query_string, result_type='recent')
        return tweets

