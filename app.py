import pandas as pd
import streamlit as st
from download import download
from forex_python.converter import CurrencyRates
import requests


def main():
    '''download()'''
    # configurações da tabela
    st.set_page_config(page_title="Lista de Moeda", 
                    page_icon=":bar_chart:",
                    layout="wide")
    # criando a tabela 
    df = pd.read_excel(
        io='Countries list.xlsx',
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=0,
        usecols='A:C'
    )
    listademoedas = []
    # divindo em colunas
    for item in df['Moedas']:
        listademoedas.append(item)

    lista2 = ['TODOS', 'TODAS', 'BTC', 'ETH', 'BTC', 'DOGE', 'LTC', 'XRP']
    for item in lista2:
        if item not in listademoedas:
            listademoedas.append(item)
    listadepaises = []
    for item in df['Paises']:
        upITEM = item.upper()
        listadepaises.append(upITEM)
    
    
    col1, col2 = st.columns([1,2])
    with col2:
        with st.form(key='searchMoeda', clear_on_submit=True):
            search_Currencies = st.text_input("Leia as regras ao lado e Digite aqui o que você está procurando").upper()
            submit_button = st.form_submit_button(label='Procurar')
            res = requests.get('http://economia.awesomeapi.com.br/json/all/{}-BRL'.format(search_Currencies))
            if submit_button:
                if search_Currencies in listadepaises:
                    search_Currencies = search_Currencies.capitalize()
                    results = df.loc[df['Paises'] == search_Currencies]
                    st.write(results)
                elif search_Currencies in listademoedas:
                    if search_Currencies not in listademoedas:
                        st.info('A moeda digitada não existe')
                    elif search_Currencies == "TODOS" or search_Currencies == "TODAS":
                        st.info('Você procurou por : Todas as moedas')
                        results = df
                        st.write(results)
                    elif search_Currencies == "BTC":
                        if res.status_code == 200:
                                moeda = res.json()[search_Currencies]['low']
                                st.info('Sabia que você ia digitar isso o preço da ' + search_Currencies + ' está em: R$' + moeda + "0,00")
                    elif search_Currencies == "ETH":
                        if res.status_code == 200:
                                moeda = res.json()[search_Currencies]['low']
                                st.info('O preço atual do ' + search_Currencies + ' está em: R$ ' + moeda + "000,00")
                    elif search_Currencies == "DOGE":
                        if res.status_code == 200:
                                moeda = res.json()[search_Currencies]['low']
                                st.info('O preço atual da ' + search_Currencies + ' está em: R$ ' + moeda)
                    elif search_Currencies == "LTC":
                        if res.status_code == 200:
                                moeda = res.json()[search_Currencies]['low']
                                st.info('O preço da ' + search_Currencies + ' está em: R$ ' + moeda + ',00')
                    elif search_Currencies == "XRP":
                        if res.status_code == 200:
                                moeda = res.json()[search_Currencies]['low']
                                st.info('O preço da ' + search_Currencies + ' está em: R$ ' + moeda + '0')
                    else:
                        if res.status_code == 200:
                            moeda = float(res.json()[search_Currencies]['low'])
                            st.info('Preço Atual: R$ {:,.2f}'.format(moeda))
                        else:
                            try:
                                c = CurrencyRates()
                                cota = c.get_rate(search_Currencies, 'BRL')
                                st.info('Preço Atual: R$ {:,.2f}'.format(cota))
                            except:
                                st.info('Moeda fora do rastreio')
                        st.info('Os seguintes Países usam {} como moeda:'.format(search_Currencies))
                        results = df.loc[df['Moedas'] == search_Currencies]
                        st.write(results)
                else:
                    st.info('{} não é um argumento valido'.format(search_Currencies))
    with col1:
        st.info('Você pode pesquisar por:')
        st.info('Nome de um País ou de uma Moeda')
        st.info('Digite todas para ver a lista completa')


if __name__ == '__main__':
    main()