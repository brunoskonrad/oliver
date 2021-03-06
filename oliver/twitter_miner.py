#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Konrad'

import tweepy
import os


class TwitterMiner(object):
    """
    Mineiradora do Twitter! O objetivo dessa classe é ir atrás de tweets afim de preencher uma base de dados.
    É interessante que já sejam buscados tweets com :) ou :( para facilitar a análise de sentimentos
    """

    # Arquivo local de credenciais do twitter
    _CREDENTIAL_FILE = '.twitter_credential'

    def __init__(self, consumer_key, consumer_secret):
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.authorize()
        self.api = tweepy.API(self._auth)

    def authorize(self):
        """
        Autoriza o objeto de API do tweepy. Seja usando as credenciais armazenadas localmente ou indo direto
        aos serviços de autenticação e autorização do Twitter. Se feito pelo Twitter salva a autorização localmente.
        """
        if not self._is_authorized:
            print (self._auth.get_authorization_url())
            try:
                self._auth.get_access_token(raw_input('Digite o token do Twitter: '))
                self.save_twitter_credentials()
            except tweepy.TweepError:
                print 'Error! Failed to get access token.'
        else:
            tokens = self.get_twitter_credentials()
            if tokens is not None:
                self._auth.set_access_token(tokens[0], tokens[1])
            else:
                os.remove(TwitterMiner._CREDENTIAL_FILE)
                raise Exception('Alguma coisa deu errado na hora de criar isso')

    def search(self, q, lang="pt", limit=15):
        return tweepy.Cursor(self.api.search, q=q, lang=lang).items(limit)

    @property
    def _is_authorized(self):
        """
        :return: se True é porque o usuário está autorizado. False senão.
        """
        return os.path.exists(TwitterMiner._CREDENTIAL_FILE)

    def save_twitter_credentials(self, key=None, secret=None):
        """
        Salva, localmente, as credenciais para autenticação do objeto de acesso a API do Twitter
        :param key: parâmetro opcional, se não for passado, usa o armazenado no objeto de autenticação OAuth do Twitter.
        É a chave de Token pública fornecida pelo Twitter após autorizar o uso da conta no App Oliver.
        :param secret: parâmetro opcional, se não for passado, usa o armazenado no objeto de autenticação OAuth do
        Twitter. É a chave de Token privada fornecida pelo Twitter após autorizar o uso da conta no App Oliver.
        :return:
        """
        if key is None:
            key = str(self._auth.access_token)
        if secret is None:
            secret = str(self._auth.access_token_secret)
        open(TwitterMiner._CREDENTIAL_FILE, 'w+').write('%s;%s' % (key, secret))

    def get_twitter_credentials(self):
        """
        Obtém as credenciais salvas localmente.
        :return: Se tiver autorizado retorna um array com a primeira casa a chave pública e a segunda a chave privada.
        Senão retorna None
        """
        if self._is_authorized:
            return open(TwitterMiner._CREDENTIAL_FILE, "r").readline().split(';')
        return None