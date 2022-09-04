import requests
import pandas as pd
from formating import treatment

def download():
    print('Your request is being processed...')
    # first thing geting the right api
    request = requests.get("https://restcountries.com/v2/all?fields=name,capital,currencies").json()

    # Creating a list for each object i'm getting so i can work on it 
    Name = []
    Capital = []
    currencies = []

    def format_float(value):
        return f'{value:_.2f}'

    # Cleaning country names
    for pais in request:
        name = pais['name']
        Name.append(name)

    # Cleaning capital names
    for city in request:
        cidade = city.get('capital')
        if cidade == None:
            Capital.append("-")
        else: 
            Capital.append(cidade)


    # Cleaning currencies 
    for moedas in request:
        moeda = moedas.get('currencies')
        if moeda == None:
            currencies.append('-')
        else:
            currencies.append(moeda)




    # starting a df from the raw request
    df = pd.DataFrame(request)
    # putting the cleaner data in the df
    df['Paises'] = Name
    df['Capitais'] = Capital
    df['Moedas'] = currencies

    # taking of the old data
    df.pop('independent')
    df.pop('name')
    df.pop('capital')
    df.pop('currencies')

    # organizing rows
    nome_coluna = ['Paises', 'Capitais', 'Moedas']
    df = df.reindex(columns=nome_coluna)

    # starting the excel writer
    writer = pd.ExcelWriter('Countries list.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='List', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    # Next cleaning phase, starting the excel reader
    Paises = pd.read_excel('Countries list.xlsx')

    # Creating a variable to split the currencies based on : to get what i need
    variable_split = Paises['Moedas'].str.split(':')
    Paises['Moedas'] = variable_split.str.get(1)
    Paises['Currencies2'] = variable_split.str.get(4)

    # Creating another variable to split it again
    variable_split2 = Paises['Moedas'].str.split(',')
    Paises['Moedas'] = variable_split2.str.get(0)
    variable_splitando = Paises['Currencies2'].str.split(',')
    Paises['Currencies2'] = variable_splitando.str.get(0)
    Paises.to_excel('Countries list.xlsx', index=False)

    # Cleaning the last column, by spliting it again
    Coins = pd.read_excel('Countries list.xlsx')
    variable_split3 = Paises['Moedas'].str.split("'")
    Paises['Moedas'] = variable_split3.str.get(1)
    variable_splitando2 = Paises['Currencies2'].str.split("'")
    Paises['Currencies2'] = variable_splitando2.str.get(1)
    Paises.to_excel('Countries list.xlsx', index=False)
    df = pd.DataFrame(['-'], columns=list('D'), index=[10])

    # Filling gaps
    data = pd.read_excel('Countries list.xlsx')
    data['Moedas'].fillna("-", inplace=True)

    # using the second curriencie to adapt the places with 2 or more currencies
    data['Currencies2'].fillna(" ", inplace=True)
    df = data
    df['Moedas'] = df['Moedas'].map(str) + "," + df['Currencies2']
    m = df["Moedas"].str.endswith(', ')
    df["Moedas"].loc[m] =  df["Moedas"].loc[m].str[:-2]
    df.pop('Currencies2')
    df.to_excel('Countries list.xlsx', index=False)
    # calling a function to treat the data
    treatment()
    print("Aquivo criado")


if __name__ == '__main__':
    download()