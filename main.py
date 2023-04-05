import locale

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from funcoes.funcoes import trata_decimal, trata_porcentagem
from modelos import FundoImobiliario, Estrategia


headers = {'User-Agent': 'Chrome'}

resposta = requests.get("https://www.fundamentus.com.br/fii_resultado.php", headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')

linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

resultado = []

estrategia = Estrategia(
    cotacao_atual_minima=50.0,
    dividend_yield_minimo=5,
    p_vp_minimo=0.70,
    valor_mercado_minimo=200000000,
    liquidez_minima=50000,
    qt_minima_imoveis=5,
    maxima_vacancia_media=10
)

for linha in linhas:
    dados = linha.find_all('td')
    codigo = dados[0].text
    segmento = dados[1].text
    cotacao_atual = trata_decimal(dados[2].text)
    ffo_yield = trata_porcentagem(dados[3].text)
    dividend_yield = trata_porcentagem(dados[4].text)
    p_vp = trata_decimal(dados[5].text)
    valor_mercado = trata_decimal(dados[6].text)
    liquidez = trata_decimal(dados[7].text)
    qt_imoveis = int(dados[8].text)
    preco_m2 = trata_decimal(dados[9].text)
    aluguel_m2 = trata_decimal(dados[10].text)
    cap_rate = trata_porcentagem(dados[11].text)
    vacancia_media = trata_porcentagem(dados[12].text)


    fundo_imb = FundoImobiliario(codigo, segmento, cotacao_atual, ffo_yield, dividend_yield, p_vp, valor_mercado,
                 liquidez, qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_media
    )


    if estrategia.aplica_estrategia(fundo_imb):
        resultado.append(fundo_imb)

cabecalho = ["CODIGO", "SEGMENTO", "COTAÇÃO ATUAL", "DIVIDEND YIELD"]

tabela = []

for elemento in resultado:
    tabela.append([
        elemento.codigo,
        elemento.segmento,
        locale.currency(elemento.cotacao_atual),
        f'{locale.str(elemento.dividend_yield)}%',
    ])

print(tabulate(tabela, headers=cabecalho, showindex='always',tablefmt='fancy_grid'))
