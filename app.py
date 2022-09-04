import pandas as pd
import plotly.express as px
import streamlit as st
from download import download
from forex_python.converter import CurrencyRates
import requests

def main():
    download()
    # configurações da tabela
    st.set_page_config(page_title="Lista de Moeda", 
                    page_icon=":bar_chart:",
                    layout="wide")
    # criando a tabela 
    df = pd.read_excel(
        io='Countries list.xlsx',
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=1,
        usecols='A:C'
    )
    listademoedas = []
    # divindo em colunas
    for item in df['Moedas']:
        listademoedas.append(item)

    lista2 = ['TODOS', 'TODAS', 'BTC', 'ETH', 'BTC', 'DOGE', 'ETH', 'LTC', 'XRP']
    for item in lista2:
        if item not in listademoedas:
            listademoedas.append(item)
    
    

    
    with st.form(key='searchMoeda', clear_on_submit=True):
        search_Currencies = st.text_input("Qual moeda você esta procurando?").upper()
        submit_button = st.form_submit_button(label='Procurar')
        res = requests.get('http://economia.awesomeapi.com.br/json/all/{}-BRL'.format(search_Currencies))
        if submit_button:
            if search_Currencies not in listademoedas:
                st.info('A moeda digitada não existe')
            elif search_Currencies == "TODOS" or search_Currencies == "TODAS":
                st.info('Você procurou por : Todas as moedas')
                results = df
                st.write(results)
            elif search_Currencies == "BTC":
                if res.status_code == 200:
                        moeda = res.json()[search_Currencies]['low']
                        st.info('Sabia que você ia digitar isso o preço da ' + search_Currencies + ' está em: R$' + moeda + ",00")
            
            else:
                col1, col2 = st.columns([3,2])
                with col1:
                    st.info('Os seguintes Países usam {} como moeda:'.format(search_Currencies))
                    results = df.loc[df['Moedas'] == search_Currencies]
                    st.write(results)
                with col2:
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



if __name__ == '__main__':
    main()