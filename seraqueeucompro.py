import urllib, simplejson

RESULT_OK = 'ok'
RESULT_ERROR = 'error'

class ChaveInvalida(Exception): pass

class Api(object):
    chave = None
    api_base_url = 'http://www.seraqueeucompro.com/api/1.0'

    def __init__(self, chave, api_base_url=None):
        global urllib

        self.chave = chave
        self.api_base_url = api_base_url or self.api_base_url

        self.set_urllib(urllib)

    def set_urllib(self, urllib):
        self._urllib = urllib

    def get_url(self, url, params=None):
        fp = self.opener.open(self.api_base_url+url, params)
        cont = fp.read()
        fp.close()

        try:
            return simplejson.loads(cont)
        except AttributeError:
            return cont

    @property
    def opener(self):
        if not hasattr(self, '_opener'):
            self._opener = self._urllib.build_opener()

        return self._opener

    def validar_chave(self, chave=None):
        chave = chave or self.chave
        cont = self.get_url('/validar-chave/?chave='+chave)

        try:
            if cont['res'] == RESULT_OK:
                return True
            else:
                raise ChaveInvalida(cont['msg'])
        except KeyError:
            self.fail('URL nao retornou resultados.')

