#!/usr/bin/python2.6
# -*- coding: utf-8 -*-#

'''Unit tests for the twitter.py library'''

__author__ = 'marinho@gmail.com'

import os, sys, simplejson, unittest, urllib

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, lib_path)

import seraqueeucompro

PERSISTENTE = False

class ApiTest(unittest.TestCase):
    chave = '12345678901234567890123456789012'
    API_BASE_URL = 'http://www.seraqueeucompro.com/api/1.0'
    
    def setUp(self):
        if PERSISTENTE:
            self._urllib = urllib
        else:
            self._urllib = MockUrllib()

        api = seraqueeucompro.Api(chave=self.chave)
        api.set_urllib(self._urllib)
        self._api = api

    def test_validar_chave(self):
        """Efetua a validacao da chave informada."""
        self._AddHandler(self.API_BASE_URL+'/validar-chave/?chave='+self.chave,
                     curry(self._OpenTestData, 'validar-chave.json'))

        self.assertTrue(self._api.validar_chave())

    def test_validar_chave_invalida(self):
        """Efetua a validacao da chave informada, sendo ela invalida."""
        self._AddHandler(self.API_BASE_URL+'/validar-chave/?chave=123',
                     curry(self._OpenTestData, 'validar-chave-invalida.json'))

        self.assertRaises(seraqueeucompro.ChaveInvalida, self._api.validar_chave, '123')

    def _AddHandler(self, url, callback):
        self._urllib.AddHandler(url, callback)

    def _OpenTestData(self, filename):
        return open(os.path.join('testdata',filename))

class MockUrllib(object):
    '''A mock replacement for urllib that hardcodes specific responses.'''

    def __init__(self):
        self._handlers = {}
        self.HTTPBasicAuthHandler = MockHTTPBasicAuthHandler

    def AddHandler(self, url, callback):
        self._handlers[url] = callback

    def build_opener(self, *handlers):
        return MockOpener(self._handlers)

class MockOpener(object):
    '''A mock opener for urllib'''

    def __init__(self, handlers):
        self._handlers = handlers
        self._opened = False

    def open(self, url, data=None):
        if self._opened:
            raise Exception('MockOpener already opened.')
        if url in self._handlers:
            self._opened = True
            return self._handlers[url]()
        else:
            raise Exception('Unexpected URL %s' % url)

    def close(self):
        if not self._opened:
            raise Exception('MockOpener closed before it was opened.')
        self._opened = False

class MockHTTPBasicAuthHandler(object):
    '''A mock replacement for HTTPBasicAuthHandler'''

    def add_password(self, realm, uri, user, passwd):
        # TODO(dewitt): Add verification that the proper args are passed
        pass


class NullCache(object):
    '''A no-op replacement for the cache class'''

    def Get(self, key):
        return None

    def Set(self, key, data):
        pass

    def Remove(self, key):
        pass

    def GetCachedTime(self, key):
        return None


class curry:
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52549

    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.fun(*(self.pending + args), **kw)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiTest))
    return suite

if __name__ == '__main__':
    unittest.main()

