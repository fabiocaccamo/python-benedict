# -*- coding: utf-8 -*-

from benedict import benedict as bdict

import unittest


class stackoverflow_questions_test_case(unittest.TestCase):

    def test_stackoverflow_question_20528081(self):
        """
        https://stackoverflow.com/questions/20528081/performance-of-calculations-on-large-flattened-dictionary-with-implied-hierarchy
        """
        d = {
            'guy1_arm_param1':23.0, 'guy1_arm_param2_low':2.0, 'guy1_arm_param2_high':3.0, 'guy1_arm_param3':20.0,
            'guy1_leg_param1':40.0, 'guy1_leg_param2_low':2.0, 'guy1_leg_param2_high':3.0, 'guy1_leg_param3':20.0,
            'guy2_arm_param1':23.0, 'guy2_arm_param2_low':2.0, 'guy2_arm_param2_high':3.0, 'guy2_arm_param3':20.0,
            'guy2_leg_param1':40.0, 'guy2_leg_param2_low':2.0, 'guy2_leg_param2_high':3.0, 'guy2_leg_param3':20.0,
            'another_guy_param1':3.0,
        }
        b = bdict(d)
        u = b.unflatten()
        # print(u.dump())
        r = {
            "another": {
                "guy": {
                    "param1": 3.0,
                },
            },
            "guy1": {
                "arm": {
                    "param1": 23.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
                "leg": {
                    "param1": 40.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
            },
            "guy2": {
                "arm": {
                    "param1": 23.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
                "leg": {
                    "param1": 40.0,
                    "param2": {
                        "high": 3.0,
                        "low": 2.0,
                    },
                    "param3": 20.0,
                },
            },
        }
        self.assertEqual(u, r)

    def test_stackoverflow_question_58692636(self):
        """
        https://stackoverflow.com/questions/58692636/python-script-fails-to-extract-data-from-xml/58695393#58695393
        """
        data_xml = """
        <feed xml:base="http://data.treasury.gov/Feed.svc/">
          <title type="text">DailyTreasuryYieldCurveRateData</title>
          <id>
            http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData
          </id>
          <updated>2019-11-04T07:15:32Z</updated>
          <link rel="self" title="DailyTreasuryYieldCurveRateData" href="DailyTreasuryYieldCurveRateData"/>
          <entry>
            <id>
              http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7258)
            </id>
            <title type="text"/>
            <updated>2019-11-04T07:15:32Z</updated>
            <author>
              <name/>
            </author>
            <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7258)"/>
            <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
            <content type="application/xml">
              <m:properties>
                <d:Id m:type="Edm.Int32">7258</d:Id>
                <d:NEW_DATE m:type="Edm.DateTime">2019-01-02T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH m:type="Edm.Double">2.4</d:BC_1MONTH>
                <d:BC_2MONTH m:type="Edm.Double">2.4</d:BC_2MONTH>
                <d:BC_3MONTH m:type="Edm.Double">2.42</d:BC_3MONTH>
                <d:BC_6MONTH m:type="Edm.Double">2.51</d:BC_6MONTH>
                <d:BC_1YEAR m:type="Edm.Double">2.6</d:BC_1YEAR>
                <d:BC_2YEAR m:type="Edm.Double">2.5</d:BC_2YEAR>
                <d:BC_3YEAR m:type="Edm.Double">2.47</d:BC_3YEAR>
                <d:BC_5YEAR m:type="Edm.Double">2.49</d:BC_5YEAR>
                <d:BC_7YEAR m:type="Edm.Double">2.56</d:BC_7YEAR>
                <d:BC_10YEAR m:type="Edm.Double">2.66</d:BC_10YEAR>
                <d:BC_20YEAR m:type="Edm.Double">2.83</d:BC_20YEAR>
                <d:BC_30YEAR m:type="Edm.Double">2.97</d:BC_30YEAR>
                <d:BC_30YEARDISPLAY m:type="Edm.Double">2.97</d:BC_30YEARDISPLAY>
              </m:properties>
            </content>
          </entry>
          <entry>
          <id>
            http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7259)
          </id>
          <title type="text"/>
          <updated>2019-11-04T07:15:32Z</updated>
          <author>
            <name/>
          </author>
          <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7259)"/>
          <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
          <content type="application/xml">
            <m:properties>
              <d:Id m:type="Edm.Int32">7259</d:Id>
              <d:NEW_DATE m:type="Edm.DateTime">2019-01-03T00:00:00</d:NEW_DATE>
              <d:BC_1MONTH m:type="Edm.Double">2.42</d:BC_1MONTH>
              <d:BC_2MONTH m:type="Edm.Double">2.42</d:BC_2MONTH>
              <d:BC_3MONTH m:type="Edm.Double">2.41</d:BC_3MONTH>
              <d:BC_6MONTH m:type="Edm.Double">2.47</d:BC_6MONTH>
              <d:BC_1YEAR m:type="Edm.Double">2.5</d:BC_1YEAR>
              <d:BC_2YEAR m:type="Edm.Double">2.39</d:BC_2YEAR>
              <d:BC_3YEAR m:type="Edm.Double">2.35</d:BC_3YEAR>
              <d:BC_5YEAR m:type="Edm.Double">2.37</d:BC_5YEAR>
              <d:BC_7YEAR m:type="Edm.Double">2.44</d:BC_7YEAR>
              <d:BC_10YEAR m:type="Edm.Double">2.56</d:BC_10YEAR>
              <d:BC_20YEAR m:type="Edm.Double">2.75</d:BC_20YEAR>
              <d:BC_30YEAR m:type="Edm.Double">2.92</d:BC_30YEAR>
              <d:BC_30YEARDISPLAY m:type="Edm.Double">2.92</d:BC_30YEARDISPLAY>
            </m:properties>
          </content>
        </entry>
        <entry>
          <id>
            http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7260)
          </id>
          <title type="text"/>
          <updated>2019-11-04T07:15:32Z</updated>
          <author>
            <name/>
          </author>
          <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7260)"/>
          <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
          <content type="application/xml">
             <m:properties>
               <d:Id m:type="Edm.Int32">7260</d:Id>
               <d:NEW_DATE m:type="Edm.DateTime">2019-01-04T00:00:00</d:NEW_DATE>
               <d:BC_1MONTH m:type="Edm.Double">2.4</d:BC_1MONTH>
               <d:BC_2MONTH m:type="Edm.Double">2.42</d:BC_2MONTH>
               <d:BC_3MONTH m:type="Edm.Double">2.42</d:BC_3MONTH>
               <d:BC_6MONTH m:type="Edm.Double">2.51</d:BC_6MONTH>
               <d:BC_1YEAR m:type="Edm.Double">2.57</d:BC_1YEAR>
               <d:BC_2YEAR m:type="Edm.Double">2.5</d:BC_2YEAR>
               <d:BC_3YEAR m:type="Edm.Double">2.47</d:BC_3YEAR>
               <d:BC_5YEAR m:type="Edm.Double">2.49</d:BC_5YEAR>
               <d:BC_7YEAR m:type="Edm.Double">2.56</d:BC_7YEAR>
               <d:BC_10YEAR m:type="Edm.Double">2.67</d:BC_10YEAR>
               <d:BC_20YEAR m:type="Edm.Double">2.83</d:BC_20YEAR>
               <d:BC_30YEAR m:type="Edm.Double">2.98</d:BC_30YEAR>
               <d:BC_30YEARDISPLAY m:type="Edm.Double">2.98</d:BC_30YEARDISPLAY>
             </m:properties>
           </content>
         </entry>
        </feed>
        """

        data = bdict.from_xml(data_xml)
        # print(data.dump())
        entries = data['feed.entry']
        for entry in entries:
            props = bdict(bdict(entry)['content.m:properties'])
            # print(props.dump())
            for key, value in props.items():
                # print(key, value['#text'])
                pass
            # print('-----')

    def test_stackoverflow_question_58827592(self):
        """
        https://stackoverflow.com/questions/58827592/is-there-a-way-to-convert-csv-columns-into-hierarchical-relationships
        """
        data_source = """
RecordID,kingdom,phylum,class,order,family,genus,species
1,Animalia,Chordata,Mammalia,Primates,Hominidae,Homo,Homo sapiens
2,Animalia,Chordata,Mammalia,Carnivora,Canidae,Canis,Canis
3,Plantae,nan,Magnoliopsida,Brassicales,Brassicaceae,Arabidopsis,Arabidopsis thaliana
4,Plantae,nan,Magnoliopsida,Fabales,Fabaceae,Phaseoulus,Phaseolus vulgaris
"""
        data_input = bdict.from_csv(data_source)
        data_output = bdict()

        ancestors_hierarchy = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
        for value in data_input['values']:
            data_output['.'.join([value[ancestor] for ancestor in ancestors_hierarchy])] = bdict()

        # print(data_output.dump())
        keypaths = sorted(data_output.keypaths(), key=lambda item: len(item.split('.')), reverse=True)

        data_output['children'] = []
        def transform_data(d, key, value):
            if isinstance(value, dict):
                value.update({ 'name':key, 'children':[] })
        data_output.traverse(transform_data)

        for keypath in keypaths:
            target_keypath = '.'.join(keypath.split('.')[:-1] + ['children'])
            data_output[target_keypath].append(data_output.pop(keypath))

        # print(data_output.dump())

    def test_stackoverflow_question_59176476(self):
        """
        https://stackoverflow.com/questions/59176476/in-python-how-to-parse-a-multi-layered-json
        """
        # data_source = 'http://legis.senado.leg.br/dadosabertos/materia/20050'
        # data = bdict.from_json('http://legis.senado.leg.br/dadosabertos/materia/20050')
        data_source = {
            'DetalheMateria': {
                '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                '@xsi:noNamespaceSchemaLocation': 'http://legis.senado.leg.br/dadosabertos/dados/DetalheMateriav5.xsd',
                'Metadados': {
                    'Versao': '03/12/2019 21:36:18',
                    'VersaoServico': '5',
                    'DataVersaoServico': '2017-02-01',
                    'DescricaoDataSet': 'Dados básicos da matéria, incluindo autoria, norma gerada e outras informações. A partir de fevereiro de 2019, os requerimentos de comissões permanentes passam a ser numerados com a mesma sistemática dos requerimentos das comissões temporárias, seguindo, portanto, o padrão: REQ 99/2019 - SIGLA_COMISSÃO. Dessa forma, para se buscar um requerimento de determinada comissão (com ano a partir de 2019), deve-se informar .../materia/sigla/número/ano?comissao=sigla da comissão.'
                },
                'Materia': {
                    'IdentificacaoMateria': {
                        'CodigoMateria': '20050',
                        'SiglaCasaIdentificacaoMateria': 'SF',
                        'NomeCasaIdentificacaoMateria': 'Senado Federal',
                        'SiglaSubtipoMateria': 'PLC',
                        'DescricaoSubtipoMateria': 'PROJETO DE LEI DA CÂMARA',
                        'NumeroMateria': '00035',
                        'AnoMateria': '1988',
                        'DescricaoObjetivoProcesso': 'Revisora',
                        'DescricaoIdentificacaoMateria': 'PLC 35/1988',
                        'IndicadorTramitando': 'Não'
                    },
                    'DadosBasicosMateria': {
                        'EmentaMateria': "DECLARA FERIADO NACIONAL O DIA 20 DE NOVEMBRO, ANIVERSARIO DA MORTE   \n      DE ZUMBI DOS PALMARES, CONSAGRADO PELA COMUNIDADE AFRO-BRASILEIRA     \n      COMO 'DIA NACIONAL DA CONSCIENCIA NEGRA.'                          \n      ",
                        'IndicadorComplementar': 'Não',
                        'DataApresentacao': '1987-12-01',
                        'DataLeitura': '1987-12-01'
                    },
                    'Autoria': {
                        'Autor': [
                            {'NomeAutor': 'Câmara dos Deputados', 'SiglaTipoAutor': 'CAMARA', 'DescricaoTipoAutor': 'Câmara dos Deputados', 'NumOrdemAutor': '1', 'IndicadorOutrosAutores': 'Não'}
                        ]
                    },
                    'Iniciativa': {
                        'SiglaTipoIniciativa': 'DEPUTADO',
                        'DescricaoTipoIniciativa': 'Deputado',
                        'DescricaoIniciativa': 'BENEDITA DA SILVA'
                    },
                    'OrigemMateria': {
                        'SiglaCasaOrigem': 'CD',
                        'NomeCasaOrigem': 'Câmara dos Deputados'
                    },
                    'CasaIniciadoraNoLegislativo': {
                        'SiglaCasaIniciadora': 'SF',
                        'NomeCasaIniciadora': 'Senado Federal'
                    },
                    'OutrosNumerosDaMateria': {
                        'OutroNumeroDaMateria': {
                            'IdentificacaoMateria': {
                                'SiglaCasaIdentificacaoMateria': 'CD',
                                'NomeCasaIdentificacaoMateria': 'Câmara dos Deputados',
                                'SiglaSubtipoMateria': 'PL',
                                'DescricaoSubtipoMateria': 'PROJETO DE LEI',
                                'NumeroMateria': '00293',
                                'AnoMateria': '1987'
                            },
                            'DescricaoTipoNumeracao': 'CasaIniciadora'
                        }
                    },
                    'SituacaoAtual': {
                        'Autuacoes': {
                            'Autuacao': [
                                {
                                    'NumeroAutuacao': '1',
                                    'Situacao': {
                                        'DataSituacao': '1996-01-23',
                                        'CodigoSituacao': '28',
                                        'SiglaSituacao': 'ARQVD',
                                        'DescricaoSituacao': 'ARQUIVADA AO FINAL DA LEGISLATURA'
                                    },
                                    'Local': {
                                        'DataLocal': '1996-01-23',
                                        'CodigoLocal': '206',
                                        'TipoLocal': 'A',
                                        'SiglaCasaLocal': 'SF',
                                        'NomeCasaLocal': 'Senado Federal',
                                        'SiglaLocal': 'SSEXP',
                                        'NomeLocal': 'SUBSECRETARIA DE EXPEDIENTE'
                                    }
                                }
                            ]
                        }
                    },
                    'OutrasInformacoes': {
                        'Servico': [
                            {
                                'NomeServico': 'EmendaMateria',
                                'DescricaoServico': 'Emendas da matéria',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/materia/emendas/20050?v=6'
                            },
                            {
                                'NomeServico': 'MovimentacaoMateria',
                                'DescricaoServico': 'Movimentações da matéria, como tramitações, despachos e prazos.\n      Evoluções:\n      14/8/2019\n      - criada nova Tag "DeliberacoesMPV" para as deliberações de MPV;\n - criada nova Tag "DescricaoItemCalendario" subord',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/materia/movimentacoes/20050?v=6'
                            },
                            {
                                'NomeServico': 'RelatoriaMateria',
                                'DescricaoServico': 'Relatoria atual e relatorias encerradas (histórico) da matéria',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/materia/relatorias/20050?v=5'
                            },
                            {
                                'NomeServico': 'TextoMateria',
                                'DescricaoServico': 'Textos da matéria. \n      Evoluções da versão: \n      28/8/2019 - incluída a tag "AutoriaTexto", sob a tag "Texto".',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/materia/textos/20050?v=5'
                            },
                            {
                                'NomeServico': 'VotacaoMateria',
                                'DescricaoServico': 'Votações da matéria',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/materia/votacoes/20050?v=5'
                            },
                            {
                                'NomeServico': 'VotacoesComissao',
                                'UrlServico': 'http://legis.senado.leg.br/dadosabertos/votacaoComissao/materia/PLC/00035/1988?v=1'
                            }
                        ]
                    },
                    'UrlGlossario': 'http://legis.senado.leg.br/dadosabertos/glossario/lista'
                }
            }
        }

        data = bdict(data_source)

        # once your url will return a valid json you could just do:
        # data = bdict.from_json('http://legis.senado.leg.br/dadosabertos/materia/20050')

        author = bdict(data[['DetalheMateria', 'Materia', 'Autoria', 'Autor']][0])
        author_name = author['NomeAutor']
        # print(author_name)
