#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Konrad'

from pymongo import MongoClient
from oliver import app_config


class MongoSentence(object):
    """
    É a classe que irá trabalhar com a inserção de dados em uma base de dados MongoDB
    """
    def __init__(self):
        self._mongo_client = MongoClient(app_config['host'], app_config['port'])

        # pega a base de dados oliver_test
        self._db_oliver = self._mongo_client['oliver_test']
        # pega a coleção onde serão inseridos os documentos
        self._sentences = self._db_oliver['sentences']

    def get_all_tweets(self):
        return self._sentences.find({'origin': 'twitter'})

    def _insert_base(self, text, origin):
        document = {
            'text': text,
            'origin': origin
        }
        return self._sentences.insert(document)

    def insert_tweets(self, search_result):
        return self._insert_base(search_result.text, 'twitter')