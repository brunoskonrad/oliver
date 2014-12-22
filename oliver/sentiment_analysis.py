#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Bruno Konrad'

import nltk
from oliver.data_sentence import MongoSentence


class SentimentAnalysis(object):

    def __init__(self):
        self._sentence = MongoSentence()
        self._pos_tweets = [('I love this car', 'positive'),
                            ('This view is amazing', 'positive'),
                            ('I feel great this morning', 'positive'),
                            ('I am so excited about the concert', 'positive'),
                            ('He is my best friend', 'positive')]
        self._neg_tweets = [('I do not like this car', 'negative'),
                            ('This view is horrible', 'negative'),
                            ('I feel tired this morning', 'negative'),
                            ('I am not looking forward to the concert', 'negative'),
                            ('He is my enemy', 'negative')]
        self._tweets = []
        for (words, sentiment) in self._pos_tweets + self._neg_tweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
            self._tweets.append((words_filtered, sentiment))
        self._test_tweets = [
            (['feel', 'happy', 'this', 'morning'], 'positive'),
            (['larry', 'friend'], 'positive'),
            (['not', 'like', 'that', 'man'], 'negative'),
            (['house', 'not', 'great'], 'negative'),
            (['your', 'song', 'annoying'], 'negative')
        ]

    def get_words_in_tweets(self):
        all_words = []
        for (words, sentiment) in self._tweets:
            all_words.extend(words)
        return all_words

    def get_word_features(self):
        wordlist = nltk.FreqDist(self.get_words_in_tweets())
        word_features = wordlist.keys()
        return word_features

    def extract_features(self, document):
        document_words = set(document)
        features = {}

        word_features = self.get_word_features()

        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def training(self):
        training_set = nltk.classify.apply_features(self.extract_features, self._tweets)
