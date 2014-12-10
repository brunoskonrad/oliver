#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Konrad'

from oliver import app_config
from oliver.twitter_miner import TwitterMiner
from oliver.data_sentence import MongoSentence


class Mole(object):
    """
    O Toupeira! Vai ser a cola do TwitterMiner e do DatabaseSaver! Vai buscar os tweets e salvar. Isso mermo.
    Acho que dá pra fazer várias Threads rodando nisso e ir salvando assim mesmo. Pode crer e pode pá.
    """
    def __init__(self):
        self._twitter_minner = TwitterMiner(app_config['consumer_key'], app_config['consumer_secret'])
        self._sentence = MongoSentence()

        #trampo_search = self._twitter_minner.api.search('trabalho :)')
        #for result in trampo_search:
        #    self._db_saver.insert_tweets(result)
        #print ('Tweets salvos...')

    def get_saved_tweets(self):
        return self._sentence.get_all_tweets()

    def search_positive_tweets(self):
        tweets = self._twitter_minner.search(':)', limit=100)
        for t in tweets:
            print(t.text)

    def _save_tweets(self, tweet):
        self._sentence.insert_tweets(tweet)