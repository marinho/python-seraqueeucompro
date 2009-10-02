import urllib, urllib2, simplejson

RESULT_OK = 'ok'
RESULT_ERROR = 'error'

class ChaveInvalida(Exception): pass
class RetornoInvalido(Exception): pass

class Api(object):
    chave = None
    api_base_url = 'http://www.seraqueeucompro.com/api/1.0'

    def __init__(self, chave, api_base_url=None):
        self.chave = chave
        self.api_base_url = api_base_url or self.api_base_url

        self.set_urllib(urllib2)

    def set_urllib(self, urllib):
        """Determina a biblioteca de captura de URL da API. Importante
        para possibilitar mockup"""
        self._urllib = urllib

    def get_url(self, url, params=None):
        """Usar a biblioteca de captura de URL para acessar uma URL e retornar
        seu conteudo. Caso o retorno seja JSON, converte o retorno antes de
        dar o resultado da funcao"""

        # Seta a chave, caso seja uma requisicao de POST
        if params:
            params.setdefault('chave', self.chave)
            params = urllib.urlencode(params)

        fp = self.opener.open(self.api_base_url+url, params)
        cont = fp.read()
        fp.close()

        try:
            return simplejson.loads(cont)
        except AttributeError:
            return cont

    @property
    def opener(self):
        """Propriedade que retorna o opener da biblioteca de URL"""

        if not hasattr(self, '_opener'):
            self._opener = self._urllib.build_opener()

        return self._opener

    def validar_retorno(self, ret):
        try:
            if ret['res'] != RESULT_OK:
                raise RetornoInvalido(ret['msg'])
        except KeyError:
            raise RetornoInvalido('URL nao retornou resultados.')

    # METODOS DA API

    def validar_chave(self, chave=None):
        """Metodo que efetua a validacao da chave informada"""

        chave = chave or self.chave
        cont = self.get_url('/validar-chave/?chave='+chave)

        try:
            self.validar_retorno(cont)
        except RetornoInvalido, e:
            raise ChaveInvalida(unicode(e))
        
        return True

    def pesquisar(self, palavras):
        """Metodo que efetua uma pesquisa pelas palavras-chave informadas"""

        palavras = urllib.quote(palavras)
        cont = self.get_url('/pesquisar/?q='+palavras)

        self.validar_retorno(cont)
        return cont['lista']

    def listar_perguntas(self, produto_id=None, produto_nome=None, produto_marca=None):
        """Metodo que retorna a lista de perguntas de um produto"""

        if produto_id:
            cont = self.get_url('/listar-perguntas/?produto_id='+str(produto_id))
        elif produto_nome and produto_marca:
            produto_nome = urllib.quote(produto_nome)
            produto_marca = urllib.quote(produto_marca)
            cont = self.get_url('/listar-perguntas/?produto_nome=%s&produto_marca=%s'%(produto_nome, produto_marca))

        self.validar_retorno(cont)
        return cont['lista']

    def listar_opinioes(self, produto_id=None, produto_nome=None, produto_marca=None):
        """Metodo que retorna a lista de opinioes de um produto"""

        if produto_id:
            cont = self.get_url('/listar-opinioes/?produto_id='+str(produto_id))
        elif produto_nome and produto_marca:
            produto_nome = urllib.quote(produto_nome)
            produto_marca = urllib.quote(produto_marca)
            cont = self.get_url('/listar-opinioes/?produto_nome=%s&produto_marca=%s'%(produto_nome, produto_marca))

        self.validar_retorno(cont)
        return cont['lista']

    def listar_links(self, produto_id=None, produto_nome=None, produto_marca=None):
        """Metodo que retorna a lista de links de um produto"""

        if produto_id:
            cont = self.get_url('/listar-links/?produto_id='+str(produto_id))
        elif produto_nome and produto_marca:
            produto_nome = urllib.quote(produto_nome)
            produto_marca = urllib.quote(produto_marca)
            cont = self.get_url('/listar-links/?produto_nome=%s&produto_marca=%s'%(produto_nome, produto_marca))

        self.validar_retorno(cont)
        return cont['lista']

    def listar_imagens(self, produto_id=None, produto_nome=None, produto_marca=None):
        """Metodo que retorna a lista de imagens de um produto"""

        if produto_id:
            cont = self.get_url('/listar-imagens/?produto_id='+str(produto_id))
        elif produto_nome and produto_marca:
            produto_nome = urllib.quote(produto_nome)
            produto_marca = urllib.quote(produto_marca)
            cont = self.get_url('/listar-imagens/?produto_nome=%s&produto_marca=%s'%(produto_nome, produto_marca))

        self.validar_retorno(cont)
        return cont['lista']

    def info_produto(self, produto_id=None, produto_nome=None, produto_marca=None):
        """Metodo que retorna as informacoes de um produto"""

        if produto_id:
            cont = self.get_url('/info-produto/?produto_id='+str(produto_id))
        elif produto_nome and produto_marca:
            produto_nome = urllib.quote(produto_nome)
            produto_marca = urllib.quote(produto_marca)
            cont = self.get_url('/info-produto/?produto_nome=%s&produto_marca=%s'%(produto_nome, produto_marca))

        self.validar_retorno(cont)
        return cont['info']

    def painel_produto_url(self, produto_id=None, produto_nome=None, produto_marca=None):
        if produto_id:
            return self.api_base_url+'/painel-produto/?produto_id='+str(produto_id)
        elif produto_nome and produto_marca:
            return self.api_base_url+'/painel-produto/?produto_nome=Fusca&produto_marca=Volkswagen'

        raise Exception('Informe o ID ou o nome e marca do produto')

    def salvar_opiniao(self, **kwargs):
        cont = self.get_url('/salvar-opiniao/', kwargs)

        self.validar_retorno(cont)

        return cont['id']

    def excluir_opiniao(self, opiniao_id):
        cont = self.get_url('/excluir-opiniao/', {'opiniao_id': opiniao_id})

        self.validar_retorno(cont)
        return True

    def salvar_pergunta(self, **kwargs):
        cont = self.get_url('/salvar-pergunta/', kwargs)

        self.validar_retorno(cont)

        return cont['id']

    def excluir_pergunta(self, pergunta_id):
        cont = self.get_url('/excluir-pergunta/', {'pergunta_id': pergunta_id})

        self.validar_retorno(cont)
        return True

    def salvar_produto(self, **kwargs):
        cont = self.get_url('/salvar-produto/', kwargs)

        self.validar_retorno(cont)

        return cont['id']

    def excluir_produto(self, produto_id):
        cont = self.get_url('/excluir-produto/', {'produto_id': produto_id})

        self.validar_retorno(cont)
        return True

