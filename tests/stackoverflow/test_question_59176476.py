import unittest


class stackoverflow_question_59176476_test_case(unittest.TestCase):
    def test_stackoverflow_question_59176476(self):
        """
        https://stackoverflow.com/questions/59176476/in-python-how-to-parse-a-multi-layered-json
        """
        from benedict import benedict as bdict

        # data_source = 'http://legis.senado.leg.br/dadosabertos/materia/20050'
        # data = bdict.from_json('http://legis.senado.leg.br/dadosabertos/materia/20050')
        data_source = {
            "DetalheMateria": {
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "@xsi:noNamespaceSchemaLocation": "http://legis.senado.leg.br/dadosabertos/dados/DetalheMateriav5.xsd",
                "Metadados": {
                    "Versao": "03/12/2019 21:36:18",
                    "VersaoServico": "5",
                    "DataVersaoServico": "2017-02-01",
                    "DescricaoDataSet": "Dados básicos da matéria, incluindo autoria, norma gerada e outras informações. A partir de fevereiro de 2019, os requerimentos de comissões permanentes passam a ser numerados com a mesma sistemática dos requerimentos das comissões temporárias, seguindo, portanto, o padrão: REQ 99/2019 - SIGLA_COMISSÃO. Dessa forma, para se buscar um requerimento de determinada comissão (com ano a partir de 2019), deve-se informar .../materia/sigla/número/ano?comissao=sigla da comissão.",
                },
                "Materia": {
                    "IdentificacaoMateria": {
                        "CodigoMateria": "20050",
                        "SiglaCasaIdentificacaoMateria": "SF",
                        "NomeCasaIdentificacaoMateria": "Senado Federal",
                        "SiglaSubtipoMateria": "PLC",
                        "DescricaoSubtipoMateria": "PROJETO DE LEI DA CÂMARA",
                        "NumeroMateria": "00035",
                        "AnoMateria": "1988",
                        "DescricaoObjetivoProcesso": "Revisora",
                        "DescricaoIdentificacaoMateria": "PLC 35/1988",
                        "IndicadorTramitando": "Não",
                    },
                    "DadosBasicosMateria": {
                        "EmentaMateria": "DECLARA FERIADO NACIONAL O DIA 20 DE NOVEMBRO, ANIVERSARIO DA MORTE   \n      DE ZUMBI DOS PALMARES, CONSAGRADO PELA COMUNIDADE AFRO-BRASILEIRA     \n      COMO 'DIA NACIONAL DA CONSCIENCIA NEGRA.'                          \n      ",
                        "IndicadorComplementar": "Não",
                        "DataApresentacao": "1987-12-01",
                        "DataLeitura": "1987-12-01",
                    },
                    "Autoria": {
                        "Autor": [
                            {
                                "NomeAutor": "Câmara dos Deputados",
                                "SiglaTipoAutor": "CAMARA",
                                "DescricaoTipoAutor": "Câmara dos Deputados",
                                "NumOrdemAutor": "1",
                                "IndicadorOutrosAutores": "Não",
                            }
                        ]
                    },
                    "Iniciativa": {
                        "SiglaTipoIniciativa": "DEPUTADO",
                        "DescricaoTipoIniciativa": "Deputado",
                        "DescricaoIniciativa": "BENEDITA DA SILVA",
                    },
                    "OrigemMateria": {
                        "SiglaCasaOrigem": "CD",
                        "NomeCasaOrigem": "Câmara dos Deputados",
                    },
                    "CasaIniciadoraNoLegislativo": {
                        "SiglaCasaIniciadora": "SF",
                        "NomeCasaIniciadora": "Senado Federal",
                    },
                    "OutrosNumerosDaMateria": {
                        "OutroNumeroDaMateria": {
                            "IdentificacaoMateria": {
                                "SiglaCasaIdentificacaoMateria": "CD",
                                "NomeCasaIdentificacaoMateria": "Câmara dos Deputados",
                                "SiglaSubtipoMateria": "PL",
                                "DescricaoSubtipoMateria": "PROJETO DE LEI",
                                "NumeroMateria": "00293",
                                "AnoMateria": "1987",
                            },
                            "DescricaoTipoNumeracao": "CasaIniciadora",
                        }
                    },
                    "SituacaoAtual": {
                        "Autuacoes": {
                            "Autuacao": [
                                {
                                    "NumeroAutuacao": "1",
                                    "Situacao": {
                                        "DataSituacao": "1996-01-23",
                                        "CodigoSituacao": "28",
                                        "SiglaSituacao": "ARQVD",
                                        "DescricaoSituacao": "ARQUIVADA AO FINAL DA LEGISLATURA",
                                    },
                                    "Local": {
                                        "DataLocal": "1996-01-23",
                                        "CodigoLocal": "206",
                                        "TipoLocal": "A",
                                        "SiglaCasaLocal": "SF",
                                        "NomeCasaLocal": "Senado Federal",
                                        "SiglaLocal": "SSEXP",
                                        "NomeLocal": "SUBSECRETARIA DE EXPEDIENTE",
                                    },
                                }
                            ]
                        }
                    },
                    "OutrasInformacoes": {
                        "Servico": [
                            {
                                "NomeServico": "EmendaMateria",
                                "DescricaoServico": "Emendas da matéria",
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/materia/emendas/20050?v=6",
                            },
                            {
                                "NomeServico": "MovimentacaoMateria",
                                "DescricaoServico": 'Movimentações da matéria, como tramitações, despachos e prazos.\n      Evoluções:\n      14/8/2019\n      - criada nova Tag "DeliberacoesMPV" para as deliberações de MPV;\n - criada nova Tag "DescricaoItemCalendario" subord',
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/materia/movimentacoes/20050?v=6",
                            },
                            {
                                "NomeServico": "RelatoriaMateria",
                                "DescricaoServico": "Relatoria atual e relatorias encerradas (histórico) da matéria",
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/materia/relatorias/20050?v=5",
                            },
                            {
                                "NomeServico": "TextoMateria",
                                "DescricaoServico": 'Textos da matéria. \n      Evoluções da versão: \n      28/8/2019 - incluída a tag "AutoriaTexto", sob a tag "Texto".',
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/materia/textos/20050?v=5",
                            },
                            {
                                "NomeServico": "VotacaoMateria",
                                "DescricaoServico": "Votações da matéria",
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/materia/votacoes/20050?v=5",
                            },
                            {
                                "NomeServico": "VotacoesComissao",
                                "UrlServico": "http://legis.senado.leg.br/dadosabertos/votacaoComissao/materia/PLC/00035/1988?v=1",
                            },
                        ]
                    },
                    "UrlGlossario": "http://legis.senado.leg.br/dadosabertos/glossario/lista",
                },
            }
        }

        data = bdict(data_source)

        # once your url will return a valid json you could just do:
        # data = bdict.from_json('http://legis.senado.leg.br/dadosabertos/materia/20050')

        author = bdict(data[["DetalheMateria", "Materia", "Autoria", "Autor"]][0])
        author_name = author["NomeAutor"]
        # print(author_name)
