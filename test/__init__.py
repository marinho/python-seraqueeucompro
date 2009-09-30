#!/usr/bin/python2.6
# -*- coding: utf-8 -*-#

'''Unit tests for the twitter.py library'''

__author__ = 'marinho@gmail.com'

import os, sys, simplejson, unittest, urllib

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, lib_path)

import seraqueeucompro

class ApiTest(unittest.TestCase):
    persistente = False
    chave = '1234567890123456789012345678901234567890'
    api_base_url = 'http://www.seraqueeucompro.com/api/1.0'
    
    def setUp(self):
        if self.persistente:
            self._urllib = urllib
        else:
            self._urllib = MockUrllib()

        api = seraqueeucompro.Api(chave=self.chave)
        api.set_urllib(self._urllib)
        self._api = api

    # TESTES - O QUE REALMENTE IMPORTA - INICIO

    def test_validar_chave(self):
        """Efetua a validacao da chave informada."""
        self._AddHandler(self.api_base_url+'/validar-chave/?chave='+self.chave,
                curry(self._OpenTestData, 'validar-chave.json'))

        self.assertTrue(self._api.validar_chave())

    def test_validar_chave_invalida(self):
        """Efetua a validacao da chave informada, sendo ela invalida."""
        self._AddHandler(self.api_base_url+'/validar-chave/?chave=123',
                curry(self._OpenTestData, 'validar-chave-invalida.json'))

        self.assertRaises(seraqueeucompro.ChaveInvalida, self._api.validar_chave, '123')

    def test_pesquisar(self):
        """Efetua uma pesquisa no site pelas palavras-chave informadas."""
        self._AddHandler(self.api_base_url+'/pesquisar/?q=produto%20encontrado',
                curry(self._OpenTestData, 'pesquisar.json'))

        lista = self._api.pesquisar('produto encontrado')
        self.assertEqual(lista, [
            {
                'titulo': 'Volkswagen Fusca 69',
                'url': 'http://www.seraqueeucompro.com/produtos/3/',
                'detalhes': 'Classico vintage da montadora alema',
                },
            {
                'titulo': 'Vale a pena comprar um Fusca original?',
                'url': 'http://www.seraqueeucompro.com/perguntas/37/',
                'detalhes': 'Estou em duvida entre um Fusca original ou restaurar um',
                },
            ])

    def test_listar_perguntas_por_id(self):
        """Efetua uma requisicao de perguntas de um produto - por ID do produto."""
        self._AddHandler(self.api_base_url+'/listar-perguntas/?produto_id=18',
                curry(self._OpenTestData, 'listar-perguntas-por-id.json'))

        lista = self._api.listar_perguntas(produto_id=18)
        self.assertEqual(lista, [
            {
                'titulo': 'Vale a pena comprar um Fusca original?',
                'url': 'http://www.seraqueeucompro.com/perguntas/37/',
                'detalhes': 'Estou em duvida entre um Fusca original ou restaurar um',
                'data': '2009-09-26 09:01:33',
                'respostas': [
                    {
                        'usuario': 'marinho@seraqueucompro.com.br',
                        'texto': 'Eu acho que voce deve comprar!',
                        'data': '2009-09-26 10:01:33',
                        },
                    ],
                },
            ])

    def test_listar_perguntas_por_nome(self):
        """Efetua uma requisicao de perguntas de um produto - por marca e nome."""
        self._AddHandler(self.api_base_url+'/listar-perguntas/?produto_nome=Fusca&produto_marca=Volkswagen',
                curry(self._OpenTestData, 'listar-perguntas-por-nome.json'))

        lista = self._api.listar_perguntas(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(lista, [
            {
                'titulo': 'Vale a pena comprar um Fusca original?',
                'url': 'http://www.seraqueeucompro.com/perguntas/32/',
                'detalhes': 'Estou em duvida entre um Fusca original ou restaurar um',
                'data': '2009-09-26 09:01:33',
                'respostas': [
                    {
                        'usuario': 'marinho@seraqueucompro.com.br',
                        'texto': 'Eu acho que voce deve comprar!',
                        'data': '2009-09-26 10:01:33',
                        },
                    ],
                },
            ])

    def test_listar_opinioes_por_id(self):
        """Efetua uma requisicao de opinioes de um produto - por ID do produto."""
        self._AddHandler(self.api_base_url+'/listar-opinioes/?produto_id=18',
                curry(self._OpenTestData, 'listar-opinioes-por-id.json'))

        lista = self._api.listar_opinioes(produto_id=18)
        self.assertEqual(lista, [
            {
                'titulo': 'Nao gostei do volante e nem do cambio',
                'url': 'http://www.seraqueeucompro.com/opinioes/37/',
                'detalhes': 'Eh isso aih',
                'data': '2009-09-26 09:01:33',
                'avaliacao': 4,
                'comentarios': [
                    {
                        'usuario': 'marinho@seraqueucompro.com.br',
                        'texto': 'Discordo!',
                        'data': '2009-09-26 10:01:33',
                        },
                    ],
                },
            ])

    def test_listar_opinioes_por_nome(self):
        """Efetua uma requisicao de opinioes de um produto - por marca e nome."""
        self._AddHandler(self.api_base_url+'/listar-opinioes/?produto_nome=Fusca&produto_marca=Volkswagen',
                curry(self._OpenTestData, 'listar-opinioes-por-nome.json'))

        lista = self._api.listar_opinioes(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(lista, [
            {
                'titulo': 'Nao gostei do volante e nem do cambio',
                'url': 'http://www.seraqueeucompro.com/opinioes/32/',
                'detalhes': 'Eh isso aih',
                'data': '2009-09-26 09:01:33',
                'avaliacao': 4,
                'comentarios': [
                    {
                        'usuario': 'marinho@seraqueucompro.com.br',
                        'texto': 'Discordo!',
                        'data': '2009-09-26 10:01:33',
                        },
                    ],
                },
            ])

    def test_listar_links_por_id(self):
        """Efetua uma requisicao de links de um produto - por ID do produto."""
        self._AddHandler(self.api_base_url+'/listar-links/?produto_id=18',
                curry(self._OpenTestData, 'listar-links-por-id.json'))

        lista = self._api.listar_links(produto_id=18)
        self.assertEqual(lista, [
            'http://www.teste.com',
            'http://pt.wikipedia.org/wiki/Fusca',
            ])

    def test_listar_links_por_nome(self):
        """Efetua uma requisicao de links de um produto - por marca e nome."""
        self._AddHandler(self.api_base_url+'/listar-links/?produto_nome=Fusca&produto_marca=Volkswagen',
                curry(self._OpenTestData, 'listar-links-por-nome.json'))

        lista = self._api.listar_links(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(lista, [
            'http://www.teste.com',
            'http://pt.wikipedia.org/wiki/Fusca',
            ])

    def test_listar_imagens_por_id(self):
        """Efetua uma requisicao de imagens de um produto - por ID do produto."""
        self._AddHandler(self.api_base_url+'/listar-imagens/?produto_id=18',
                curry(self._OpenTestData, 'listar-imagens-por-id.json'))

        lista = self._api.listar_imagens(produto_id=18)
        self.assertEqual(lista, [
            'http://localhost:8080/imagens/30/',
            'http://teste.com/foto.jpg',
            ])

    def test_listar_imagens_por_nome(self):
        """Efetua uma requisicao de imagens de um produto - por marca e nome."""
        self._AddHandler(self.api_base_url+'/listar-imagens/?produto_nome=Fusca&produto_marca=Volkswagen',
                curry(self._OpenTestData, 'listar-imagens-por-nome.json'))

        lista = self._api.listar_imagens(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(lista, [
            'http://localhost:8080/imagens/30/',
            'http://teste.com/foto.jpg',
            ])

    def test_produto_info_por_id(self):
        """Efetua uma requisicao de informacoes de um produto - por ID do produto."""
        self._AddHandler(self.api_base_url+'/info-produto/?produto_id=18',
                curry(self._OpenTestData, 'info-produto-por-id.json'))

        info = self._api.info_produto(produto_id=18)
        self.assertEqual(info, {
            'nome': 'Fusca',
            'marca': 'Volkswagen',
            'url': 'http://www.seraqueeucompro.com/produtos/18/',
            'produto_url': 'http://www.fusca.com',
            'categoria': 'Automoveis',
            'slug': 'fusca',
            'tags': ['carros','esporte','classicos'],
            'descricao': 'O Fusca foi o carro mais vendido da historia do automovel',
            })

    def test_produto_info_por_nome(self):
        """Efetua uma requisicao de informacoes de um produto - por marca e nome."""
        self._AddHandler(self.api_base_url+'/info-produto/?produto_nome=Fusca&produto_marca=Volkswagen',
                curry(self._OpenTestData, 'info-produto-por-nome.json'))

        info = self._api.info_produto(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(info, {
            'nome': 'Fusca',
            'marca': 'Volkswagen',
            'url': 'http://www.seraqueeucompro.com/produtos/18/',
            'produto_url': 'http://www.fusca.com',
            'categoria': 'Automoveis',
            'slug': 'fusca',
            'tags': ['carros','esporte','classicos'],
            'descricao': 'O Fusca foi o carro mais vendido da historia do automovel',
            })

    def test_produto_painel_url_por_id(self):
        """Efetua uma requisicao de informacoes de um produto - por ID do produto."""
        url = self._api.painel_produto_url(produto_id=18)
        self.assertEqual(url, self.api_base_url+'/painel-produto/?produto_id=18')

    def test_produto_painel_url_por_nome(self):
        """Efetua uma requisicao de informacoes de um produto - por marca e nome."""
        url = self._api.painel_produto_url(produto_nome='Fusca', produto_marca='Volkswagen')
        self.assertEqual(url, self.api_base_url+'/painel-produto/?produto_nome=Fusca&produto_marca=Volkswagen')

    def test_opiniao_salvar_inclusao(self):
        """Efetua a inclusao de uma opiniao"""
        self._AddHandler(self.api_base_url+'/salvar-opiniao/',
                curry(self._OpenTestData, 'salvar-opiniao-inclusao.json'))

        self.assertTrue(self._api.salvar_opiniao(
            produto_nome='Fusca',
            produto_marca='Volkswagen',
            titulo='Nao gostei do volante e nem do cambio',
            detalhes='Eh isso aih',
            avaliacao=4,
            ))

    def test_opiniao_salvar_atualizacao(self):
        """Efetua a atualizacao de uma opiniao"""
        self._AddHandler(self.api_base_url+'/salvar-opiniao/',
                curry(self._OpenTestData, 'salvar-opiniao-atualizacao.json'))

        self.assertTrue(self._api.salvar_opiniao(
            opiniao_id=18,
            titulo='Nao gostei do volante e nem do cambio - novo nome',
            detalhes='Eh isso aih',
            avaliacao=5,
            ))

    def test_opiniao_salvar_invalido(self):
        """Efetua a atualizacao de uma opiniao que retorna invalido"""
        self._AddHandler(self.api_base_url+'/salvar-opiniao/',
                curry(self._OpenTestData, 'salvar-opiniao-invalido.json'))

        self.assertRaises(seraqueeucompro.RetornoInvalido, self._api.salvar_opiniao, 
            opiniao_id=15,
            titulo='Nao gostei do volante e nem do cambio - novo nome',
            detalhes='Eh isso aih',
            avaliacao=5,
            )

    def test_opiniao_excluir(self):
        """Efetua a exclusao de uma opiniao"""
        self._AddHandler(self.api_base_url+'/excluir-opiniao/',
                curry(self._OpenTestData, 'excluir-opiniao.json'))

        self.assertTrue(self._api.excluir_opiniao(opiniao_id=15))

    def test_pergunta_salvar_inclusao(self):
        """Efetua a inclusao de uma pergunta"""
        self._AddHandler(self.api_base_url+'/salvar-pergunta/',
                curry(self._OpenTestData, 'salvar-pergunta-inclusao.json'))

        self.assertTrue(self._api.salvar_pergunta(
            produto_nome='Fusca',
            produto_marca='Volkswagen',
            titulo='Compro original ou reformo?',
            detalhes='Teste',
            ))

    def test_pergunta_salvar_atualizacao(self):
        """Efetua a atualizacao de uma pergunta"""
        self._AddHandler(self.api_base_url+'/salvar-pergunta/',
                curry(self._OpenTestData, 'salvar-pergunta-atualizacao.json'))

        self.assertTrue(self._api.salvar_pergunta(
            pergunta_id=18,
            titulo='Compro original ou reformo?',
            detalhes='Teste',
            ))

    def test_pergunta_salvar_invalido(self):
        """Efetua a atualizacao de uma pergunta que retorna invalido"""
        self._AddHandler(self.api_base_url+'/salvar-pergunta/',
                curry(self._OpenTestData, 'salvar-pergunta-invalido.json'))

        self.assertRaises(seraqueeucompro.RetornoInvalido, self._api.salvar_pergunta, 
            pergunta_id=15,
            titulo='Compro original ou reformo?',
            detalhes='Teste',
            )

    def test_pergunta_excluir(self):
        """Efetua a exclusao de uma pergunta"""
        self._AddHandler(self.api_base_url+'/excluir-pergunta/',
                curry(self._OpenTestData, 'excluir-pergunta.json'))

        self.assertTrue(self._api.excluir_pergunta(pergunta_id=15))

    # TESTES - O QUE REALMENTE IMPORTA - FINAL

    def _AddHandler(self, url, callback):
        self._urllib.AddHandler(url, callback)

    def _OpenTestData(self, filename):
        return open(os.path.join('testdata',filename))

#class ApiPersistenteTest(ApiTest):
#    persistente = True
#    api_base_url = 'http://localhost:8080/api/1.0'

class MockUrllib(object):
    '''A mock replacement for urllib that hardcodes specific responses.'''

    def __init__(self):
        self._handlers = {}

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

