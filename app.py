import pandas as pd
import streamlit as st
from download import download
from forex_python.converter import CurrencyRates
import requests



 # configurações da tabela
st.set_page_config(page_title="Lista de Moeda", 
                page_icon=":money_with_wings:",
                layout="wide")


@st.cache
def pegando_os_dados_do_exel():
    # criando a tabela 
    df = pd.read_excel(
        io='Countries list.xlsx',
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=0,
        usecols='A:C'
    )
    return df


df = pegando_os_dados_do_exel()


def streamlit_scene():
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
                        st.info('Lista completa')
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
        st.subheader('Opções disponíveis:')
        st.caption('Nome de um País ou de uma Moeda')
        st.caption('Digite todas para ver a lista completa')
        st.subheader('Conversor')
        option = st.selectbox(
        'Escolha uma moeda',
        ('USD', 'EUR', 'BRL'))
        option2 = st.selectbox(
        'Para',
        ('BRL', 'USD', 'EUR'))
        link = ('http://economia.awesomeapi.com.br/json/all/' + option + '-' + option2)
        res2 = requests.get(link)
        if res2.status_code == 200:
            moeda1 = float(res2.json()[option]['low'])
            with st.form(key='conversor'):
                convertendo = float(st.number_input("Digite o valor a ser Convertido:"))
                submit_button = st.form_submit_button(label='Converter')
                if option2 == 'USD':
                    total = convertendo * moeda1
                    st.info(f'Valor convertido: $ {total:.2f}')
                elif option2 == 'EUR':
                    total = convertendo * moeda1
                    st.info(f'Valor convertido: € {total:.2f}')
                else:
                    total = convertendo * moeda1
                    st.info(f'Valor convertido: R$ {total:.2f}')


# confgs da pagina

st.markdown("<h1 style='text-align: center; color: white;'>Lista de paises e suas Moedas</h1>", unsafe_allow_html=True)
st.markdown('---')

# usando css para esconder as coisas da pagina
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)         
if __name__ == '__main__':
    pegando_os_dados_do_exel()
    streamlit_scene()   