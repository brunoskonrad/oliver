#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Konrad'

from oliver.data_sentence import MongoSentence


class SentimentAnalysis(object):

    def __init__(self):
        self._sentence = MongoSentence()