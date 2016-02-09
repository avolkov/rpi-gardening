#!/usr/bin/env python

import tweepy
from ConfigParser import ConfigParser

from soil_moisture import needs_watering

msg = "Alex, please water me. I'm a plant. I need water"


def authorize_tweepy(configfile):
    auth = tweepy.OAuthHandler(
        configfile.get('settings', 'consumer_key'),
        configfile.get('settings', 'consumer_secret')
    )
    auth.set_access_token(
        configfile.get('settings', 'access_key'),
        configfile.get('settings', 'access_secret')
    )
    return tweepy.API(auth)


if __name__ == "__main__":
    config = ConfigParser()
    config.readfp(open('settings.ini'))
    twitter_api = authorize_tweepy(config)

    if needs_watering():
        twitter_api.update_status(msg)
